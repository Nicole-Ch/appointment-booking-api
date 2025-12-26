from django.contrib import admin
from django.urls import path , include
from .views import AppointmentListView, AppointmentSlotRetrieve,AppointmentSlotList,ServiceTypeList,ServiceTypeRetrieve,AppointmentCreateView,SlotCreateView, AppointmentCancelView,AppointmentRescheduleView, AppointmentFeedbackCreate


urlpatterns = [
  


   path('service/', ServiceTypeList.as_view(), name='services' ), #View available services
   path('service/<int:pk>/', ServiceTypeRetrieve.as_view, name='serviceDetail'),# view service detail
   path('slot/', AppointmentSlotList.as_view(), name='slots'), #view appointment slots
   path('slot/<int:pk>', AppointmentSlotRetrieve.as_view(), name='slotDetail'), #view slot details

   path('slot/create/' , SlotCreateView.as_view(), name='slot-create'), #provider creates a slot
   path('appointment/create', AppointmentCreateView.as_view(), name='appointment-create'), #customer creates appointment
   path("appointments/", AppointmentListView.as_view(), name="appointment-list"), #list of ll appointments

   path('appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),#Cancel an Appointment
    path("appointments/<int:pk>/reschedule/", AppointmentRescheduleView.as_view(), name="appointment-reschedule"), #Reschedule an Appointment
    path('appointment/<int:pk>/feedback/', AppointmentFeedbackCreate.as_view(), name='appointment-feedback')#feedback for an appointment
   


]

