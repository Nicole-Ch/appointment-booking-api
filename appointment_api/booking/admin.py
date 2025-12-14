from django.contrib import admin
from .models import ServiceType , Appointment, AppointmentSlot, Feedback
# Register your models here.

admin.site.register(ServiceType)
admin.site.register(Appointment)
admin.site.register(AppointmentSlot)
admin.site.register(Feedback)