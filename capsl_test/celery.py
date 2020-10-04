import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capsl_test.settings')

app = Celery('capsl_test')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='')

@app.task
def test():
    print('hello world!')

app.conf.beat_schedule = {
    'print-every-30-seconds': {
        'task': 'capsl_test.celery.test',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'UTC'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
