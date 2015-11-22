#!venv/bin/python

from crontab import CronTab

user_cron = CronTab(user='aasoliz')

job = user_cron.new(command='/home/aasoliz/Documents/Other/Commands/py/bitStats/job.sh')

job.minute.on(0)
job.day.every(1)

user_cron.write_to_user(user='aasoliz')
print user_cron.render()

assert job.is_valid()