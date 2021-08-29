import os
from loggr import logger
from PIL import Image
from subprocess import check_output
import config


def do_replace_path(domain, original_string, new_string):
    command = [
        "sudo", "-u", "www-data",
        "wp", "search-replace", original_string, new_string,
        "wp_post*",
        "--all-tables-with-prefix", f"--url={domain}"
                                    "--dry-run",
        "--path=" + config.get().get('APP_PATH')
    ]
    output = check_output(command)
    logger.info(output)


def replace_path(domain, original_path, new_path):
    # Remove system path prefix
    original_string = original_path.replace(os.path.join(config.get().get('APP_PATH'), "wp-content/uploads/"), "")
    new_string = new_path.replace(os.path.join(config.get().get('APP_PATH'), "wp-content/uploads/"), "")
    do_replace_path(domain, original_string, new_string)

    # Replace json encoded strings
    original_string = original_string.replace("/", "\\/")
    new_string = new_string.replace("/", "\\/")
    do_replace_path(domain, original_string, new_string)


def convert(f_image, webp_image):
    if f_image.endswith(".gif"):
        convert_gif2webp(f_image, webp_image, config.get().get('GIF_QUALITY'))
    else:
        convert_2webp(f_image, webp_image)


def convert_gif2webp(f_image, webp_image, quality):
    quality = {"quality": quality}
    im = Image.open(f_image)
    im.save(webp_image, 'webp', **quality, duration=im.info["duration"], save_all=True)


def convert_2webp(f_image, webp_image):
    im = Image.open(f_image).convert("RGB")
    im.save(webp_image, "webp")
    im.close()
