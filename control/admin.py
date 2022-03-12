from django.contrib import admin
from .models import *


@admin.register(Announce)
class AnnounceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'body',
    )


@admin.register(IPVisitant)
class IPVisitantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ip',
        'created_at',
    )


@admin.register(TodayYesterday)
class TodayYesterdayAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'today',
        'yesterday',
        'created_at',
    )
