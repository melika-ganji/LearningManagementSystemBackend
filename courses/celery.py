from celery.schedules import crontab
from celery import Celery

app = Celery('lms')

app.conf.beat_schedule = {
    'calculate-daily-revenue': {
        'task': 'courses.tasks.calculate_total_revenue',
        'schedule': crontab(hour=23, minute=59),
    },
}
