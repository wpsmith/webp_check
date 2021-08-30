#!/usr/bin/env python3

import os
import sys
import re
import webp
import config
import cloudflare
from loggr import logger

purge_cache = False

def webp_check(file_dir):
    files_done = _webp_check(file_dir)

    # Maybe clear the cache.
    cfg = config.get()
    if len(files_done) > 0 and cfg.get('CF_PURGE_CACHE'):
        print("clearing cache")
        cloudflare.purge(cfg.get('CF_ZONE_ID'))

def _webp_check(file_dir):
    files_done = []
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
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
                        files_done.append(f_path)

                        # TODO Wrap with try
                        webp.convert(f_path, w_path)
                        logger.info(f"'{f_path}' Converted to '{w_path}'")
                        print(f"'{f_path}' Converted to '{w_path}'")

            elif os.path.isdir(f_path):
                # If not a file but directory, be recursive.
                recursive_files_done = _webp_check(f_path)
                if len(recursive_files_done) > 0:
                    files_done += recursive_files_done
    else:
        logger.error(f"'{file_dir}' either doesn't exist, or is not a dir...")
        print(f"'{file_dir}' either doesn't exist, or is not a dir...")

    return files_done


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
