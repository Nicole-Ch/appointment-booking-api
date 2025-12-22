from django.shortcuts import render
from .models import Feedback, CustomUser,Appointment,AppointmentSlot,  ServiceType
from rest_framework import generics ,  permissions
from .serializers import AppointmentSerializer,AppointmentSlotSerializer,CustomUserSerializer,FeedbackSerializer, ServiceTypeSerializer,AppointmentCreateSerializer,SlotCreateSerializer
from . permissions import IsProvider
# Create your views here.


class ServiceTypeList(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]

class ServiceTypeRetrieve(generics.RetrieveAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]

class AppointmentSlotList(generics.ListAPIView):
    queryset = AppointmentSlot.objects.select_related("provider", "service_type").all()
    serializer_class = AppointmentSlotSerializer
    permission_classes = [permissions.AllowAny]

class AppointmentSlotRetrieve(generics.RetrieveAPIView):
    queryset = Appointment.objects.select_related("provider", "service_type").all()
    serializer_class = AppointmentSlotSerializer 
    permission_classes = [permissions.AllowAny] 


# Appointment Slot-Creation  
class SlotCreateView(generics.CreateAPIView):
    serializer_class = SlotCreateSerializer
    permission_classes = [permissions.IsAuthenticated,IsProvider]

    def perform_create(self, serializer):
        # ensure provider cannot create slots for another user
        provider = self.request.user
         # save the new slot and set its provider
        serializer.save(provider=provider)

