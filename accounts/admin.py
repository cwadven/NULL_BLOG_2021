from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        'is_staff',
        'is_active',
        'date_joined',
        'last_login',
    )
    search_fields = (
        'username',
        'email',
        'nickname',
    )
    list_display = (
        'id',
        'username',
        'email',
        'nickname',
        'first_name',
        'last_name',
        'date_joined',
        'is_staff',
        'is_active',
        'last_login',
    )


@admin.register(UserProvider)
class UserProviderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_editable = (
        'name',
    )
