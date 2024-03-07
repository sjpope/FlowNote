from .celery import app as celery_app

__all__ = ('celery_app',) # Celery app is to load when the app kicks off
