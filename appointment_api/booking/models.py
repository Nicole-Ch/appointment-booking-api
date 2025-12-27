from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class CustomUser(AbstractUser):
     email = models.EmailField('email address', unique=True)
     is_provider  = models.BooleanField(default=False)

     USERNAME_FIELD = "email"
     REQUIRED_FIELDS = ["username"]  

     def __str__(self):
        return self.email

class ServiceType(models.Model):
    
    name = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    #Converting duration to a human-readable format
    @admin.display(description="Duration", ordering="duration")
    def get_duration(self):

        if self.duration is None:
            return "00:00"
        total_minutes = int(self.duration)
        hours, minutes = divmod(total_minutes, 60)

        return f"{hours:02d}hours:{minutes:02d}minutes"

    def __str__(self):
         return  f"{self.name}-> Duration-({self.get_duration()})"

class AppointmentSlot(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="appointmentProvider", on_delete=models.PROTECT)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL,null=True, related_name="appointmentService")    
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["provider", "start_time"]),
        ] #Helps us easily identify an Appointment slot

        constraints = [
            models.UniqueConstraint(fields=["provider", "start_time","end_time"], name="unique_provider_slot")

        ]#Helps us avoid exact duplicate of a slot with same provider and the booking times


    def __str__(self):
        #If there is a provider, this tries to get the email attribute from the provider object.
        provider_display = getattr(self.provider, 'email', str(self.provider)) if self.provider else "unspecified"

        if self.start_time:
            start = timezone.localtime(self.start_time).isoformat()
        else:
            start = "Unspecified"

        if self.end_time:
            end = timezone.localtime(self.end_time).isoformat() 
        else:
            end = "Unspecified"       
        return f"{provider_display} | {start} - {end}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Booked", "Booked"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed")
    ]
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE, related_name="appointment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True, related_name="appointments" )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Booked")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment {self.pk} - {self.slot} by {self.user}"

class Feedback(models.Model):
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="appointmentFeedback")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )   
    rating = models.PositiveSmallIntegerField(default=0, help_text="Rating out of 5")
    comment =  models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Feedback {self.pk} (rating={self.rating})"