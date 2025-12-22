from django.shortcuts import render
from .models import Feedback, CustomUser,Appointment,AppointmentSlot,  ServiceType
from rest_framework import generics ,  permissions , status
from .serializers import AppointmentSerializer,AppointmentSlotSerializer,CustomUserSerializer,FeedbackSerializer, ServiceTypeSerializer,AppointmentCreateSerializer,SlotCreateSerializer
from . permissions import IsProvider
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
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
         # save the new slot and set its provider -ensures the provider field always matches the logged-in user.
        serializer.save(provider=provider)


#Appointment Creation
class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
       serializer = self.get_serializer(data=request.data) #return a serializer instance for AppointmentCreateSerializer
       serializer.is_valid(rase_exception = True)
       slot = serializer.validated_data['slot']

       with transaction.atomic():
           locked_slot = (AppointmentSlot.objects.select_for_update().select_related(provider).get(pk=slot.pk))

           if locked_slot.is_booked and getattr(locked_slot, 'appointment'):
             raise ValidationError({"slot": "This slot has already been booked"})
           
           appointment = Appointment.objects.create(
               slot=locked_slot,
               user=request.user,
               notes=serializer.validated_data.get("notes", ""),
           )
           locked_slot.is_booked = True
           locked_slot.save(update_fields=['is_booked'])

       out_serializer = AppointmentSerializer(appointment,context={"request":request})
       return Response(out_serializer.data, status=status.HTTP_201_CREATED)  