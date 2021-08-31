import os
import subprocess
from urllib import request

from crontab import CronTab


def install_cron():
    cron = CronTab()
    cron.new(command='my command', comment='my comment')

    job = cron.new(command='python ' + os.path.join(os.path.dirname(__file__), "webp_check.py"))
    job.minute.every(1)
    job.hour.every(1)

    cron.write()


def download_wp_cli():
    wp_cli_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "wp")
    request.urlretrieve("https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar", wp_cli_path)
    subprocess.call(["chmod", "+x", wp_cli_path])
    subprocess.call(["sudo", "mv", wp_cli_path, "/usr/local/bin/wp2"])
    output = subprocess.check_output(["wp", "--info"])
    print(output)


download_wp_cli()
