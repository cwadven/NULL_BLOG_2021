from django.contrib import admin

from notification.models import (
    NotificationType,
    ReplyNotification,
    NotificationController,
    LikeNotification,
    RereplyNotification
)


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_editable = (
        'name',
    )


@admin.register(NotificationController)
class NotificationControllerTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'representative_message',
        'is_checked',
    )


@admin.register(ReplyNotification)
class ReplyNotificationTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )


@admin.register(RereplyNotification)
class RereplyNotificationTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )


@admin.register(LikeNotification)
class LikeNotificationTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )

