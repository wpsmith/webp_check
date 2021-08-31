#!/usr/bin/env python3
from datetime import datetime
import sys
import os
import re

import cloudflare
import config
import webp
import wp
from loggr import logger

db_prefix, db_prefix_err = wp.DBPrefix().run()
app_path = config.get().get("APP_PATH").rstrip("/")


def get_backup_filename(date=""):
    if "" == date:
        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    cfg = config.get()
    path = cfg.get("BACKUPS_PATH")
    if not os.path.exists(path):
        os.makedirs(path)

    domain = cfg.get("SITE_DOMAIN")
    if domain is None:
        domain = 'wordpress'
    return os.path.join(path, f'backup-{domain}-{date}.sql')


# Import DB
def import_db(date):
    db_import = wp.DBImport(
        get_backup_filename(date),
        skip_optimizations=True,
        as_sudo=(not os.geteuid() == 0),
    )
    return db_import.run()


# Backup DB
def export_db():
    export = wp.DBExport(
        get_backup_filename(),
        add_drop_table=True,
        as_sudo=(not os.geteuid() == 0),
    )
    return export.run()


# Gets the hostname/site domain from config.
def get_domain():
    return config.get().get("SITE_DOMAIN")


# Gets the app path from config.
def get_path():
    return app_path


# Gets the URL pattern for a domain (without http/s) to an image.
def get_domain_pattern():
    return f'({get_domain()})([-a-zA-Z0-9()@:%_\+.~#?&\/=]+?([\w\d_-]+)\.)(jpg|jpeg|png|gif)'


# Gets the path pattern for a domain to an image.
def get_path_pattern():
    return f'({get_path()})([-a-zA-Z0-9()@:%_\+.~#?&\/=]+?([\w\d_-]+)\.)(jpg|jpeg|png|gif)'


# Gets the file path from URL.
def get_file(url):
    path = re.sub(rf'https?:\/\/{get_domain()}\/', "", url)
    return os.path.join(get_path(), path)


# Get DB Prefix.
def get_db_prefix():
    return db_prefix


# Purges the WP and Cloudflare cache.
def purge_cache():
    was_flushed = True
    out, err = wp.CacheFlush(
        as_sudo=(not os.geteuid() == 0),
    ).run()
    if "Success: The cache was flushed." != out.strip():
        was_flushed = False

    if config.get().get("CF_PURGE_CACHE"):
        is_flushed = cloudflare.purge(config.get().get("CF_ZONE_ID"))
        if not is_flushed:
            was_flushed = False

    return was_flushed


# Prepares the DB for this script to run and test.
def prepare():
    out, err = export_db()
    logger.info(out)
    logger.debug(err)


# Get image paths from search output for a specific table.
def get_image_paths_from_table_out(out):
    image_paths = []
    domain_matches = re.findall(get_domain_pattern(), out)
    for match in domain_matches:
        image_paths.append(os.path.join(get_path(), match[1].lstrip("/")) + match[3])

    path_matches = re.findall(get_path_pattern(), out)
    for match in path_matches:
        image_paths.append(os.path.join(get_path(), match[1].lstrip("/")) + match[3])

    return list(set(image_paths))


# Get image paths by table.
def get_image_paths_by_table(out):
    tables = {}
    matches = re.findall(r'(\w+):(\w+):(\d+):(.*)', out)
    for match in matches:
        if match[0] not in tables:
            tables[match[0]] = {"table": match[0], "out": '', "images": []}
        tables[match[0]]["out"] += "\n".join(match)

    for key, table in tables.items():
        tables[key]["images"] = get_image_paths_from_table_out(table["out"])

    return tables


# Process images, starting with the database.
def process_db_images():
    purge_cache = False

    # Find all the images.
    s = wp.DBSearch(
        get_domain_pattern(),
        as_sudo=(not os.geteuid() == 0),
        regex=True,
        all_tables=True,
        table_column_once=True,
        one_line=True,
    )
    out, err = s.run()
    print(out)
    print(err)

    # Process the images
    table_images = get_image_paths_by_table(out)
    # for table in table_images:
    for key, table in table_images.items():
        images_processed, images_not_processed, images_converted = process_images(table["images"])
        for o_file in images_converted:
            sr = wp.SearchReplace(
                o_file.replace(get_path(), ""),
                get_webp_image_file(o_file).replace(get_path(), ""),
                table=table["table"],
                as_sudo=(not os.geteuid() == 0),
                skip_themes=True,
                skip_plugins=True,
                color=False)
            out, e = sr.run()
            print(out)
            # print(err)

    return purge_cache


def get_image_exts():
    return ["jpg", "jpeg", "png", "gif"]


def process_dir(file_dir):
    dir_images_processed, dir_images_not_processed, dir_images_converted = [], [], []
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        print(f"Processing DIR {file_dir}")
        file_dir = file_dir.rstrip("/") + "/"
        files = os.listdir(file_dir)
        files = [os.path.join(file_dir, f) for f in files]
        dirs = [f for f in files if os.path.isdir(f)]
        files = [f for f in files if os.path.isfile(f) and f.split('.')[-1:][0] in get_image_exts()]

        if len(files) > 0:
            images_processed, images_not_processed, images_converted = process_images(files)
            dir_images_processed += images_processed
            dir_images_not_processed += images_not_processed
            dir_images_converted += images_converted

        for d in dirs:
            images_processed, images_not_processed, images_converted = process_dir(d)
            dir_images_processed += images_processed
            dir_images_not_processed += images_not_processed
            dir_images_converted += images_converted
    else:
        msg = f"'{file_dir}' either doesn't exist, or is not a dir..."
        logger.error(msg)
        print(msg)

    return dir_images_processed, dir_images_not_processed, dir_images_converted


def print_msgs(action, images):
    logger.info(f"---- {action.upper()} ----")
    logger.info(images)
    logger.info(f"---------------------------------")


def get_webp_image_file(o_file):
    ext = o_file.split('.')[-1:][0]
    return o_file.replace(f".{ext}", '.webp')


def process_images(image_paths):
    images_processed = []
    images_converted = []
    images_not_processed = []
    for o_file in image_paths:
        logger.debug(f"  -Processing FILE {o_file}")
        if o_file.endswith(tuple(get_image_exts())):
            w_file = get_webp_image_file(o_file)
            if os.path.exists(o_file):
                if not os.path.exists(w_file):
                    webp.convert(o_file, w_file)
                    logger.info(f"'{o_file}' Converted to '{w_file}'")
                    images_converted.append(o_file)
                else:
                    logger.debug(f"'{w_file}' exists")
                images_processed.append(o_file)
            else:
                logger.error(f"Original '{o_file}' does not exist")
                images_not_processed.append(o_file)
        else:
            logger.error(f"'{o_file}' not an image")
            images_not_processed.append(o_file)

    return images_processed, images_not_processed, images_converted


def run():
    # all_images_processed, all_images_not_processed, all_images_converted = [], [], []
    fs_images_processed, fs_images_not_processed, fs_images_converted = process_dir(get_path())
    print_msgs("filesystem images processed", fs_images_processed)
    print_msgs("filesystem images converted", fs_images_converted)
    print_msgs("filesystem images not processed", fs_images_not_processed)

    db_images_processed, db_images_not_processed, db_images_converted = process_db_images()
    print_msgs("DB images - processed", db_images_processed)
    print_msgs("DB images - converted", db_images_converted)
    print_msgs("DB images - not processed", db_images_not_processed)

    if len(fs_images_converted or db_images_converted) > 0:
        purge_cache()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app_path = sys.argv[1]
    prepare()
    # run()
