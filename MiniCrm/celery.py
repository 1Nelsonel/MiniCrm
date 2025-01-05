import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MiniCrm.settings")

# Instantiate Celery app
app = Celery("MiniCrm")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks from installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
