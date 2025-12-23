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

class SlotCreateSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(read_only=True)
    #PrimaryKeyRelatedField(read_only=True) tells DRF:
    #“This existing model relationship should be represented by its ID, and the client cannot set it.”

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'provider', 'service_type', 'start_time', 'end_time', 'is_booked']

    def validate(self, attrs):
          # Using attrs.get() to safely access the 'start_time' and 'end_time' keys
        start = attrs.get('start_time')
        end = attrs.get('end_time')
        if start and end and start >= end:
            raise serializers.ValidationError("Start time should be before end time")
        return attrs    
    
class AppointmentCreateSerializer(serializers.ModelSerializer):
    slot  = serializers.PrimaryKeyRelatedField(queryset=AppointmentSlot.objects.all()) #customer selects an existing slot by ID

    class Meta:
        model = Appointment
        fields = ['id', 'slot', 'notes']  

class AppointmentRescheduleSerializer(serializers.Serializer):

    slot = serializers.PrimaryKeyRelatedField(queryset = AppointmentSlot.objects.all())

    def validate_slot(self, value):
        return value # return the "cleaned" value
