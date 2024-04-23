import os
import platform
from celery import Celery
from celery.signals import worker_process_init
from multiprocessing import current_process
import ctypes
from ctypes import wintypes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowNoteSettings.settings')

# @worker_process_init.connect
# def configure_worker_process(*args, **kwargs):
#     process_name = current_process().name
#     print(f"Configuring {process_name}...")

#     os_name = platform.system()
#     print(f"Operating System: {os_name}")

#     try:
#         if os_name == "Windows":
#             # Modifies the working set size of the process in Windows
#             # Removes min and max constraints with -1 flag -- size is now managed dynamically.
#             # If you paid attention in CS 3339 you'd know. It's using RAM as a cache.
#             ctypes.windll.kernel32.SetProcessWorkingSetSize(ctypes.windll.kernel32.GetCurrentProcess(), -1, -1)
#             print("Configured Windows process working set size to be managed by the system.")
#         elif os_name == "Linux":
#             # Increase file descriptor limit but only for the current process
#             os.system('ulimit -n 4096')
#         elif os_name == "Darwin":
#             # macOS-specific settings
#             # MacOS uses Darwin kernel, but they could've just called it macOS.
#             # This increases maximum number of open files
#             os.system('ulimit -n 4096')
#         else:
#             print(f"You're running VSCode on a Nintendo Switch?? No specific configuration for {os_name}.")
#     except Exception as e:
#         print(f"Error configuring {process_name} for {os_name}: {str(e)}")

app = Celery('FlowNoteSettings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.update(
#     broker_url='django://',
#     result_backend='django-db',
# )