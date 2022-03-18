from django.urls import path
from .views import *

app_name = 'notification'

urlpatterns = [
    path('', get_notification, name='get_notification'),
]
