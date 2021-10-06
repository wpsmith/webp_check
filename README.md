# WP Convert Images to WebP

This replaces png, jpg, jpeg, and gif images with a webp image in the WordPress database.

Written by Travis Smith (@wpsmith)

## Summary

The program does the following:

* Creates a WordPress database backup placing it at `BACKUPS_PATH`, defaulting to `/var/www/backups`
* Searches the WordPress database for any and all png, jpg, jpeg, and gif images, creates a webp image replacement, and
  replaces the image in the database. For attachments, the attachment metadata will also be updated to the webp version.
* Searches the application path's filesystem recursively creating webp images for all remaining images.
* Clears the WordPress and Cloudflare caches based on the configuration.

While the checker can be run as root, it is highly advised that you do not run it as root. Instead it should be run with
whichever user your WordPress application is running.

## Dependencies

User must have the following installed in their environment for this to work.

### System Requirements

* Python 3.6+
* [WP CLI](https://wp-cli.org)

### Python Requirements

This only requires the following Python libraries (as can be seen via `requirements.txt`):

* requests
* pillow
* python-dotenv
* PyYAML
* python-crontab

## Installation

If you do not know whether you have these dependencies, you can run `./install.sh`, which will:

* Check your version of Python to ensure you have v3.6+ installed.
* Check for the WP CLI binary and install it for you if it is not.
* If you meet both requirements, it will:
    * install the required Python dependencies
    * installs a cronjob to run every 15 minutes

## Setup

To configure, rename `.env.default` to `.env` (e.g., `mv .env.default .env`). In this file, you will find the following
environment variables:

* `CF_API_KEY` - The Cloudflare API Key to clear the cache.
* `CF_PURGE_CACHE` - Whether or not to clear the Cloudflare cache.
* `CF_ZONE_ID` - The Cloudflare Zone ID.
* `SITE_DOMAIN` - Site domain (e.g., example.com)
* `FLUSH_DATABASE` - Whether or not to clear the WordPress cache.
* `GIF_QUALITY` - Quality of GIF.
* `APP_PATH` - WordPress application path.
* `BACKUPS_PATH` - Backups application path.
* `LOG_PATH` - Log path.
* `WP_CLI_YML` - WP CLI file path. If you do not have a `wp-cli.yml`, you can use the provided `wp-cli.sample.yml` file
  by renaming it to `wp-cli.yml` and the checker will use that file (supposedly).

## Troubleshooting

*Database Backup Error*
You may get an error backing up the database.

```
Errors: mysqldump: Can't create/write to file '/var/www/backups/backup-example.com-2021-08-31-20-49-04.sql' (OS errno 13 - Permission denied)
```

If you get this error, try the following:

* Add the `mysql` user (or whichever user is defined in `my.cnf`) to the app user group (
  e.g., `sudo usermod -aG $(stat -c '%G' $BACKUPS_PATH) mysql`).
* Change the permissions appropriately for backups and logs.

```
find $BACKUPS_PATH -type d -exec chmod 775 {} \;
find $BACKUPS_PATH -type f -exec chmod 664 {} \;
find $LOGS_PATH -type d -exec chmod 775 {} \;
find $LOGS_PATH -type f -exec chmod 664 {} \;
```

## TO DO

* Make installation interactive.
    * Get SITE_DOMAIN
    * Get APP_PATH
    * Get WP_USER (a WordPress admin username)
* Proper testing.
