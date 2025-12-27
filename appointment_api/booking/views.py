from django.shortcuts import render
from .models import Feedback, CustomUser,Appointment,AppointmentSlot,  ServiceType
from rest_framework import generics ,  permissions , status
from .serializers import AppointmentSerializer,AppointmentSlotSerializer,CustomUserSerializer,FeedbackSerializer, ServiceTypeSerializer,AppointmentCreateSerializer,SlotCreateSerializer,AppointmentRescheduleSerializer
from . permissions import IsProvider
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
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
       serializer.is_valid(raise_exception = True)
       slot = serializer.validated_data['slot'] #slot is an AppointmentSlot instance

       with transaction.atomic():
           locked_slot = (AppointmentSlot.objects.select_for_update().select_related("provider").get(pk=slot.pk))

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


class AppointmentListView(generics.ListAPIView):
    
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if getattr(Appointment, "is_provider", False):
            return Appointment.objects.select_related("slot__provider", "slot__service_type", "user").filter(
                slot__provider = user #only include appointments whose related slot’s provider equals the current user.
            ).order_by('created_at')
        
        return Appointment.objects.select_related("slot__provider", "slot__service_type").filter(
            user=user
        ).order_by("created_at")
    

#Appointment Cancel
class AppointmentCancelView(APIView):
    permission_class = [permissions.IsAuthenticated]

    def put(self,pk,request):

        try:
            appt = Appointment.objects.select_related("slot__provider").get(pk=pk)
        except Appointment.DoesNotExist:
            raise NotFound("Appointment Does not Exist")  

        user = request.user
        slot_provider = appt.slot.provider

        if not(user == appt.user or user == slot_provider or getattr(user, 'is_staff', False)):
            raise PermissionDenied("You are not allowed to cancel this appointment")

        if appt.status == "cancelled":
            raise ValidationError("This appointment is already cancelled")

        with transaction.atomic():
            appt.status = "cancelled"
            appt.save (update_field=["status"])
            appt.slot.is_booked = "False"
            appt.slot.save(update_fields='is_booked')

        out = AppointmentSerializer(appt, context = {'request': request})
        return Response(out.data, status=status.HTTP_200_OK)

#Appointment Reschedule
class AppointmentRescheduleView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self,request,pk):
        serializer = AppointmentRescheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception= True)  
        new_slot = serializer.validated_data['slot']

        try:
            appt = Appointment.objects.select_related('slot__provider').get(pk=pk)
        except Appointment.DoesNotExist:
            raise NotFound("Appointment Not Found")

        user = request.user
        slot_provider = appt.slot.provider
        old_slot = appt.slot

        #Who can reschedule an appointment
        if not(user==appt.user or user==slot_provider or getattr(user,'is_staff', False)):
           raise PermissionDenied("You can't Reschedule an Appointment")


        if new_slot.pk == old_slot.pk:
            raise ValidationError("You picked the same slot")  
        
        if new_slot.provider_id != old_slot.provider_id:
          raise ValidationError({"slot": "You must choose a slot from the same provider"})


       #Lock the slot ids
        slot_ids = [old_slot.pk, new_slot.pk]
        #ordering ids to avoid deadlocks
        slot_ids_sorted = sorted(set(slot_ids)) 
                                                                    
        with transaction.atomic():
            locked_slot_qs = AppointmentSlot.objects.select_for_update().filter(pk__in=slot_ids_sorted)

            locked = {s.pk: s for s in locked_slot_qs}

            locked_old = locked.get(old_slot.pk)   
            locked_new = locked.get(new_slot.pk)   


            if locked_new is None:
                raise NotFound("New slot not found")
            
            if locked_new.is_booked or Appointment.objects.filter(slot=locked_new).exists():
                raise ValidationError({"slot": "The requested slot is already booked"})
            
            #performing the switch
            appt.slot = locked_new
            appt.save(update_fields=['slot'])

            if locked_old:
                locked_old.is_booked = False
                locked_old.save(update_fields=['is_booked'])
            locked_new.is_booked = True
            locked_new.save(update_fields=["is_booked"])    

        out = AppointmentSerializer(appt, context={'request':request})
        return Response(out.data, status=status.HTTP_200_OK)    


class AppointmentFeedbackCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
 

    def put(self, request, pk):

        try:
            apptFeedback = Appointment.objects.select_related('slot__provider').get(pk=pk)
        except Appointment.DoesNotExist:
            raise NotFound("Appointment Does not Exist")

        #Only who created appointment can leave feedback
        if request.user !=  apptFeedback.user:
            raise ValidationError("Only user who created this appointment can leave a Feedback")
        
        if  apptFeedback.status != "Completed":
            raise ValidationError("Appointment has to be completed to leave Feedback")
        
        if hasattr( apptFeedback, 'appointmentFeedback'):
            raise ValidationError("This appointment already has a Feedback")
        

        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)          

        feedback = Feedback.objects.create(
            appointment =  apptFeedback,
            user = request.user,
            rating = serializer.validated_data['rating'],
            comment=serializer.validated_data.get("comment", "")
            

        )  

        return Response({"id": feedback.pk, "rating": feedback.rating, "comment": feedback.comment}, status=status.HTTP_201_CREATED)