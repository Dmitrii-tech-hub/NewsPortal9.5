from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .tasks import send_weekly_newsletter

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_weekly_newsletter,
        trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        id="weekly_newsletter",
        max_instances=1,
        replace_existing=True,
    )
    register_events(scheduler)
    scheduler.start()

    print("Scheduler started...")
