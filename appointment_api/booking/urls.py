from django.contrib import admin
from django.urls import path , include
from .views import AppointmentSlotRetrieve,AppointmentSlotList,ServiceTypeList,ServiceTypeRetrieve


urlpatterns = [
   path('service/', ServiceTypeList.as_view(), name='services' ),
   path('service/<int:pk>/', ServiceTypeRetrieve.as_view, name='serviceDetail'),
   path('slot/', AppointmentSlotList.as_view(), name='slots'),
   path('slot/<int:pk>', AppointmentSlotRetrieve.as_view(), name='slotDetail')

]

