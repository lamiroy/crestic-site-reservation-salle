from django.urls import path

from .views import *

urlpatterns = [
    path('holiday.ics', export_holiday_ics, name='holiday.ics'),
    path('bookedrooms.ics', export_bookedrooms_ics, name='bookedrooms.ics')
]
