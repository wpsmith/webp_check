import os

from crontab import CronTab

# Installs the cron job.
def install_cron():
    cron = CronTab()
    job = cron.new(command=os.path.join(os.path.dirname(__file__), "check"))
    job.minute.every(15)
    # job.hour.every(1)

    cron.write()


install_cron()
