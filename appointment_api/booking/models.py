from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

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
    duration = models.DateTimeField(help_text="Duration in minutes")

    def __str__(self):
         return  f"{self.name} ({self.duration_minutes}m)"

class AppointmentSlot(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="appointmentprovider", on_delete=models.PROTECT)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL,null=True, related_name="appointmentslots")    
    
    start_time = models.TimeField()
    end_time = models.TimeField()
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


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Booked", "Booked"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed")
    ]
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name="slots")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()

class Feedback(models.Model):
    RATING_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="feedbacks")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE )   
    rating = models.CharField(max_length=3, choices=RATING_CHOICES, default="1")
    comment =  models.TextField()

