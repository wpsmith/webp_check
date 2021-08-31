import os
from PIL import Image
import config
import wp

def replace_path(domain, original_path, new_path):
    # Remove system path prefix
    original_string = original_path.replace(os.path.join(config.get().get('APP_PATH'), "wp-content/uploads/"), "")
    new_string = new_path.replace(os.path.join(config.get().get('APP_PATH'), "wp-content/uploads/"), "")
    wp.search_replace(domain, original_string, new_string)

    # Replace json encoded strings
    original_string = original_string.replace("/", "\\/")
    new_string = new_string.replace("/", "\\/")
    wp.search_replace(domain, original_string, new_string)


def convert(f_image, webp_image=''):
    if '' == webp_image:
        ext = f_image.split('.')[-1:][0]
        webp_image = f_image.replace(ext, 'webp')

    if f_image.endswith(".gif"):
        convert_gif2webp(f_image, webp_image, int(config.get().get('GIF_QUALITY')))
    else:
        convert_2webp(f_image, webp_image)


def convert_gif2webp(f_image, webp_image, quality):
    quality = {"quality": quality}
    im = Image.open(f_image)
    if im.info.get('duration'):
        im.save(webp_image, 'webp', **quality, duration=im.info["duration"], save_all=True)
    else:
        im.save(webp_image, 'webp', **quality, save_all=True)


def convert_2webp(f_image, webp_image):
    im = Image.open(f_image).convert("RGB")
    im.save(webp_image, "webp")
    im.close()
