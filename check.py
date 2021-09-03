#!/usr/bin/env python3
import json
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

# ENUMs for actions taken.
CONVERTED = "converted"
PROCESSED = "processed"
NOT_PROCESSED = "not_processed"


# Gets the backup filename.
def get_backup_filename(date=""):
    """
    Gets the backup filename.
    :param date: str, optional
    :return: str
    """
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
    """
    Restores the DB using WP CLI `wp db export`.
    :return: tuple of output
    """
    db_import = wp.DBImport(
        get_backup_filename(date),
        skip_optimizations=True,
        as_sudo=(os.geteuid() == 0),
    )
    return db_import.run()


# Backup DB
def export_db():
    """
    Backups the DB using WP CLI `wp db export`.
    :return: tuple of output
    """
    export = wp.DBExport(
        get_backup_filename(),
        add_drop_table=True,
        as_sudo=(os.geteuid() == 0),
    )
    return export.run()


# Gets the hostname/site domain from config.
def get_domain():
    """
    Gets the hostname/site domain from config.
    :return: str
    """
    return config.get().get("SITE_DOMAIN")


# Gets the app path from config.
def get_path():
    """
    Gets the app path from config using the global `app_path`.
    :return: str
    """
    return app_path


# Gets the URL pattern for a domain (without http/s) to an image.
def get_domain_pattern():
    """
    Gets the URL pattern for a domain (without http/s) to an image.
    :return: str
    """
    return f'({get_domain()})([-a-zA-Z0-9()@:%_\+.~#?&\/=]+?([\w\d_-]+)\.)(jpg|jpeg|png|gif)'


# Gets the path pattern for a domain to an image.
def get_path_pattern():
    """
    Gets the path pattern for a domain to an image.
    :return: str
    """
    return f'({get_path()})([-a-zA-Z0-9()@:%_\+.~#?&\/=]+?([\w\d_-]+)\.)(jpg|jpeg|png|gif)'


# Get DB Prefix.
def get_db_prefix():
    """
    Gets DB Prefix.
    :return: str
    """
    return db_prefix


# Purges the WP and Cloudflare cache.
def purge_cache():
    """
    Purges the WP and Cloudflare cache.
    :return: bool whether cache was cleared or not.
    """
    was_flushed = True
    out, err = wp.CacheFlush(
        as_sudo=(os.geteuid() == 0),
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
    """
    Creates a backup of the DB for this script to run.
    :return: void
    """
    out, err = export_db()
    logger.info(out)
    logger.debug(err)


# Get image paths from search output for a specific table.
def get_image_paths_from_table_out(out):
    """
    Get image paths from search output for a specific table.
    :param out: String of wp db search output for a specific table.
    :return: list of image paths.
    """
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
    """
    Get image paths by table.
    :param out: String of wp db search output.
    :return: Tables object.
        {
            "table": "", Table name
            "out": "",   wp db search output for that table
            "ids": [],   IDs of the DB rows
        }
    """
    tables = {}
    matches = re.findall(r'(\w+):(\w+):(\d+):(.*)', out)

    for match in matches:
        if match[0] not in tables:
            tables[match[0]] = {"table": match[0], "out": '', "images": [], "ids": {}}
        tables[match[0]]["out"] += "\n".join(match)

        if match[1] not in tables[match[0]]["ids"]:
            tables[match[0]]["ids"][match[1]] = []
        tables[match[0]]["ids"][match[1]].append(match[2])

    for key, table in tables.items():
        tables[key]["images"] = get_image_paths_from_table_out(table["out"])

    return tables


# Process images, starting with the database.
def process_db_images():
    """
    Process images, starting with the database.
    :return: Tuple of images processed, not processed, converted
    """
    db_images_processed, db_images_not_processed, db_images_converted = [], [], []

    # Find all the images.
    s = wp.DBSearch(
        get_domain_pattern(),
        as_sudo=(os.geteuid() == 0),
        regex=True,
        all_tables=True,
        # table_column_once=True,
        one_line=True,
    )
    out, err = s.run()
    logger.info(out)
    logger.debug(err)

    # Process the images
    table_images = get_image_paths_by_table(out)

    # Process attachments first.
    if f"{get_db_prefix()}posts" in table_images and "guid" in table_images[f"{get_db_prefix()}posts"]["ids"]:
        table = table_images[f"{get_db_prefix()}posts"]

        # Only attachments will match in the guid...most likely.
        for index, ID in enumerate(table["ids"]["guid"]):
            # Get the Post.
            pg = wp.PostGet(ID, format="json", fields="post_type,post_mime_type,guid")
            out, err = pg.run()
            post = json.loads(out)

            # Maybe convert the image.
            o_file = re.sub(rf"https?:\/\/{get_domain()}", get_path(), post["guid"])
            w_file = get_webp_image_file(o_file)
            result = process_image(o_file)

            # Don't do anything else if the image was not processed.
            if NOT_PROCESSED == result:
                continue

            # Update webp image and mime type.
            if "attachment" == post["post_type"]:
                guid = re.sub(rf'({"|".join(get_image_exts())})', 'webp', post["guid"])

                # Update the post guid, post_mime_type.
                # Cannot update via wp_update_post (wp.PostUpdate).
                dbq = wp.DBQuery(f"UPDATE {table['table']} "
                                 f"SET guid=\"{guid}\", post_mime_type = \"image/webp\" "
                                 f"WHERE ID = {ID}")
                out, err = dbq.run()
                logger.info(f"Updating attachment ({ID})")
                logger.info(out)
                logger.debug(err)

                # Maybe regenerate the attachment metadata.
                # Currently there is no WP CLI command to do this sadly.
                # I probably should write one for them.
                e = wp.Eval(f"$data = wp_generate_attachment_metadata({ID}, '{w_file}');" +
                            f"if ( wp_update_attachment_metadata({ID}, $data) && update_attached_file( {ID}, '{w_file}' ) ) " + "{"
                                                                                                                                "  echo 'true';"
                                                                                                                                "} else { "
                                                                                                                                f"  throw Exception('Could not update attachment metadata for {ID}'); "
                                                                                                                                "}")
                out, err = e.run()
                logger.info(out)
                logger.debug(err)

    # for table in table_images:
    for key, table in table_images.items():

        # Now process the remaining images.
        images_processed, images_not_processed, images_converted = process_images(table["images"])
        db_images_processed += images_processed
        db_images_not_processed += images_not_processed
        db_images_converted += images_converted

        # Do all processed images.
        for o_file in images_processed:
            sr = wp.SearchReplace(
                o_file.replace(get_path(), ""),
                get_webp_image_file(o_file).replace(get_path(), ""),
                table=table["table"],
                as_sudo=(os.geteuid() == 0),
                skip_themes=True,
                skip_plugins=True,
                include_columns=",".join(table["ids"].keys()),
                all_tables=True,
                color=False)
            out, err = sr.run()
            logger.info(sr)
            logger.info(out)
            logger.debug(err)

    return db_images_processed, db_images_not_processed, db_images_converted


# Gets the supported image file extensions.
def get_image_exts():
    """
    Gets the supported image file extensions.
    :return: List of extensions
    """
    return ["jpg", "jpeg", "png", "gif"]


# Processes a directory.
def process_dir(file_dir):
    """
    Processes a directory.
    :param file_dir: File directory string
    :return: Tuple of images processed, not processed, converted
    """
    dir_images_processed, dir_images_not_processed, dir_images_converted = [], [], []
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        logger.info(f"Processing DIR {file_dir}")
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


# Prints the summary.
def print_summary(action, images):
    """
    Prints a summary.
    :param action: ENUM of actions.
    :param images: List of image filenames
    :return: void
    """
    logger.info(f"---- {action.upper()} ----\n{images}\n---------------------------------")


# Gets the webp image file from the original file.
def get_webp_image_file(o_file):
    """
    Gets the webp image file from the original file.
    :param o_file: Filepath string.
    :return: webp filepath string.
    """
    ext = o_file.split('.')[-1:][0]
    return o_file.replace(f".{ext}", '.webp')


# Processes a single image file, converting to webp.
def process_image(o_file):
    """
    Processes a single image file, converting to webp.
    :param o_file: Filepath string.
    :return: ENUM of processing result.
    """
    if o_file.endswith(tuple(get_image_exts())):
        w_file = get_webp_image_file(o_file)
        if os.path.exists(o_file):
            if not os.path.exists(w_file):
                webp.convert(o_file, w_file)
                logger.info(f"'{o_file}' Converted to '{w_file}'")
                return CONVERTED

            logger.debug(f"'{w_file}' exists")
            return PROCESSED

        logger.error(f"Original '{o_file}' does not exist")
        return NOT_PROCESSED

    logger.error(f"'{o_file}' not an image")
    return NOT_PROCESSED


# Processes a set of image files, converting them to webps.
def process_images(image_paths):
    """
    Processes a set of image files, converting them to webps.
    :param image_paths: List of image paths.
    :return: Tuple of string of filenames.
    """
    images_processed = []
    images_converted = []
    images_not_processed = []
    for o_file in image_paths:
        logger.debug(f"  -Processing FILE {o_file}")
        action = process_image(o_file)
        if "converted" == action:
            images_converted.append(o_file)

        if "converted" == action or "processed" == action:
            images_processed.append(o_file)

        if "not_processed" == action:
            images_not_processed.append(o_file)

    return images_processed, images_not_processed, images_converted


# RUNS everything.
def run():
    """
    Runs everything.
    :return: void
    """
    # all_images_processed, all_images_not_processed, all_images_converted = [], [], []
    fs_images_processed, fs_images_not_processed, fs_images_converted = process_dir(get_path())
    print_summary("filesystem images processed", fs_images_processed)
    print_summary("filesystem images converted", fs_images_converted)
    print_summary("filesystem images not processed", fs_images_not_processed)

    db_images_processed, db_images_not_processed, db_images_converted = process_db_images()
    print_summary("DB images - processed", db_images_processed)
    print_summary("DB images - converted", db_images_converted)
    print_summary("DB images - not processed", db_images_not_processed)

    if len(fs_images_converted or db_images_converted) > 0:
        purge_cache()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app_path = sys.argv[1]
    prepare()
    run()
