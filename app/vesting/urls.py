"""
URL mappings for the uer API.
"""
from django.urls import path
from vesting import views

app_name = 'vesting'

urlpatterns = [
    path('schedule/',
         views.ScheduleViewSet.as_view({'post': 'create'}), name='schedule'),
]
