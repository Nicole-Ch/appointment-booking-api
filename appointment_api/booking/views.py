from django.shortcuts import render
from .models import Feedback, CustomUser,Appointment,AppointmentSlot,  ServiceType
from rest_framework import generics ,  permissions
from .serializers import AppointmentSerializer,AppointmentSlotSerializer,CustomUserSerializer,FeedbackSerializer, ServiceTypeSerializer
# Create your views here.


class ServiceTypeList(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]

class ServiceTypeRetrieve(generics.RetrieveAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

class AppointmentSlotList(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSlotSerializer
    permission_classes = [permissions.AllowAny]

class AppointmentSlotRetrieve(generics.RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSlotSerializer            
