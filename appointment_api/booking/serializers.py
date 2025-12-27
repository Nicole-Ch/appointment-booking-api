from rest_framework import serializers
from .models import ServiceType, CustomUser, AppointmentSlot, Appointment, Feedback
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_chars = 6)

    class meta:
        model = User
        fields = ['username', 'email', 'password']



        def validate_email(self, value):
            if User.objects.filter(email__iexact=value).exists(): #find rows whose email field equals value, ignoring case.
                raise serializers.ValidationError("A user with this email already exists")
            return value
            
        def validate_username(self,value):
            if User.objects.filter(username__iexact=value).exists():
                raise serializers.ValidationError("A user with this name already exists")
            return value

        def create(self,validated_data):
            newuser = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password']
            )
            return newuser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)






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
