from rest_framework import serializers
from .models import ServiceType, CustomUser, AppointmentSlot, Appointment, Feedback


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_provider']


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = "__all__"


class AppointmentSlotSerializer(serializers.ModelSerializer):
    provider = CustomUserSerializer(read_only = True)


    class Meta:
        model = AppointmentSlot
        fields = ['id', 'provider', 'service_type', 'start_time', 'end_time', 'is_booked']

class AppointmentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only = True) #Customer Info
    slot = AppointmentSlotSerializer(read_only = True)


    class Meta:
        model = Appointment
        fields = ['id', 'user', 'slot', 'status', 'created_at', 'notes']

class FeedbackSerializer(serializers.ModelSerializer):
   
    user = CustomUserSerializer(read_only = True)

    class Meta:
        model = Feedback
        fields = ['appointment' , 'user', 'rating', 'comment', 'created_at']

