from django.contrib import admin
from django.urls import path , include
from .views import AppointmentListView, AppointmentSlotRetrieve,AppointmentSlotList,ServiceTypeList,ServiceTypeRetrieve,AppointmentCreateView,SlotCreateView


urlpatterns = [
   path('service/', ServiceTypeList.as_view(), name='services' ),
   path('service/<int:pk>/', ServiceTypeRetrieve.as_view, name='serviceDetail'),
   path('slot/', AppointmentSlotList.as_view(), name='slots'),
   path('slot/<int:pk>', AppointmentSlotRetrieve.as_view(), name='slotDetail'),

   path('slot/create/' , SlotCreateView.as_view(), name='slot-create'),
   path('appointment/create', AppointmentCreateView.as_view(), name='appointment-create'),
   path("appointments/", AppointmentListView.as_view(), name="appointment-list"),

]

