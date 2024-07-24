from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from user.management.commands.send_reminders import Command

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler, "cron", minute="*/1", replace_existing=True)
    def timed_job():
        Command().handle()

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
