from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'nickname',
        'first_name',
        'last_name',
        'date_joined',
        'is_staff',
        'is_active',
        'last_login',
    )
