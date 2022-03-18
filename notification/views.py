import json

from django.http import HttpResponse

from notification.models import NotificationController


def get_notification(request):
    notification_infos = []

    if request.user.is_authenticated and request.user.has_notifications:
        notification_set = NotificationController.objects.select_related(
            'replynotification__reply__post',
            'rereplynotification__rereply__post',
            'likenotification__like',
            'notification_type',
            'receiver',
            'sender',
        ).filter(
            receiver=request.user,
            is_checked=False,
        ).order_by('-id')

        for notification in notification_set:
            one_to_one_table = getattr(notification, notification.notification_type.name)
            notification_infos.append(one_to_one_table.get_ajax_notification_response())

    return HttpResponse(json.dumps({'notification_infos': notification_infos}), 'application/json')
