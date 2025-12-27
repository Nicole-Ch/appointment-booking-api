import os
import sys

path = "/home/Nicole/appointment-booking-api"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "appointment_api.settings"
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
