from django.contrib import admin
from .models import CustomUser, ServiceType , Appointment, AppointmentSlot, Feedback
# Register your models here.


class CustomuserAdmin(admin.ModelAdmin):
    list_display = ("email"," is_provider")

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "duration")

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id","user" , "slot" , "status" , "notes") 

class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ("provider", "service_type", "start_time", "end_time", "is_booked")   

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "appointment", "rating", "created_at")       


admin.site.register(CustomUser, CustomuserAdmin)    
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AppointmentSlot, AppointmentSlotAdmin)
admin.site.register(Feedback, FeedbackAdmin)