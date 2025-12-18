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
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
         return  f"{self.name} ({self.duration}m)"

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
        return f"{self.provider} | {self.start_time.isoformat()} - {self.end_time.isoformat()}"

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
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="AppointmentFeedback")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )   
    rating = models.PositiveSmallIntegerField(default=0, help_text="Rating out of 5")
    comment =  models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Feedback {self.pk} (rating={self.rating})"