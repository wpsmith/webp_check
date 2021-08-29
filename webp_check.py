#!/usr/bin/env python3

import os
import sys
import re
import webp
import config
import cloudflare
from loggr import logger


def webp_check(file_dir):
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        purge_cache = False
        if not file_dir[-1] == "/":
            file_dir = file_dir + "/"
        files = os.listdir(file_dir)

        # Cycle through files.
        for f in files:
            f_path = file_dir + f

            # Make sure we have a file.
            if os.path.isfile(f_path):
                ext = f_path.split('.')[-1]
                if ext == "jpg" or ext == "jpeg" or ext == "png" or ext == "gif":
                    # check if webp equivalent exists.
                    ext = f_path.split('.')[-1:][0]
                    w_path = f_path.replace(ext, 'webp')
                    if not os.path.exists(w_path):
                        # TODO Wrap with try
                        webp.convert(f_path, w_path)
                        logger.info(f"'{f_path}' Converted to '{w_path}'")
                        print(f"'{f_path}' Converted to '{w_path}'")
                        purge_cache = True

            elif os.path.isdir(f_path):
                # If not a file but directory, be recursive.
                webp_check(f_path)

        # Maybe clear the cache.
        cfg = config.get()
        if purge_cache and cfg.get('CF_PURGE_CACHE'):
            cloudflare.purge(cfg.get('CF_ZONE_ID'))
    else:
        logger.error(f"'{file_dir}' either doesn't exist, or is not a dir...")
        print(f"'{file_dir}' either doesn't exist, or is not a dir...")


def convert_image_links(post_content):
    domain = re.escape(config.get().get('SITE_DOMAIN'))
    # find image links and save to array
    links = re.findall(r'https?://' + domain + '[/|.|\w|\s|-]*\.(?:jpe?g|png)', post_content)

    # replace \.(jpg|jpeg|png) w/ .webp
    for l in links:
        ext = l.split('.')[-1:][0]
        new_link = l.replace(ext, 'webp')
        post_content = post_content.replace(l, new_link)

    # return post content
    return post_content


if __name__ == '__main__':
    if len(sys.argv) > 1:
        webp_check(sys.argv[1])
    else:
        print("missing argument...")
        exit(1)
