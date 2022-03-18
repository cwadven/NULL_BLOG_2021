import json

from django.http import HttpResponse

from accounts.models import User
from notification.models import NotificationController


def get_notification(request):
    # if request.is_ajax():
    notification_infos = []

    user = User.objects.get(user=request.user)

    # if profile.recent != profile.alert:
    #     profile.alert = profile.recent
    #     profile.save(update_fields=['alert'])

    notification_set = NotificationController.objects.select_related(
        'replynotification__reply__post',
        'rereplynotification__rereply__post',
        'likenotification__like',
        'notification_type',
        'receiver',
        'sender',
    ).filter(
        receiver=user,
        is_checked=False,
    ).order_by('-id')[:5]

    for notification in notification_set:
        one_to_one_table = getattr(notification, notification.notification_type.name)
        notification_infos.append(one_to_one_table.get_ajax_notice_response())

    return HttpResponse(json.dumps({'notification_infos': notification_infos}), 'application/json')
