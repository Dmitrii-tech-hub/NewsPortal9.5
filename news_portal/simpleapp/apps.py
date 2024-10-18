import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.apps import AppConfig
from django.db.utils import OperationalError  # Для обработки ошибок базы данных
from django.conf import settings  # Для проверки, что это не команда миграции

class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):
        if 'runserver' in sys.argv:  # Запускаем только при выполнении runserver
            try:
                from .tasks import send_weekly_posts  # Импорт задачи для рассылки
                start_scheduler()  # Запуск планировщика
            except OperationalError:
                logging.error("Database is not ready yet, scheduler not started.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        send_weekly_posts,
        trigger='interval',
        weeks=1,  # Раз в неделю
        id='weekly_posts',
        replace_existing=True
    )

    try:
        scheduler.start()
        logging.info("Scheduler started!")
    except Exception as e:
        logging.error(f"Scheduler failed to start: {e}")
