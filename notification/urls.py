from django.urls import path
from .views import *

app_name = 'notification'

urlpatterns = [
    path('', get_notification, name='get_notification'),
    path('/check/<int:notification_id>', check_notification, name='check_notification'),
]
