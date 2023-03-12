import json

from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from board.models import Reply, Rereply
from notification.models import NotificationController


def get_notification(request):
    notification_infos = []

    if request.user.is_authenticated and request.user.has_notifications:
        notification_set = NotificationController.objects.select_related(
            'replynotification__reply__post',
            'rereplynotification__rereply__post',
            'likenotification__like__post',
            'notification_type',
            'receiver',
            'sender',
        ).filter(
            receiver=request.user,
            is_checked=False,
        ).order_by('-id')

        for notification in notification_set:
            try:
                one_to_one_table = getattr(notification, notification.notification_type.name)
                notification_infos.append(one_to_one_table.get_ajax_notification_response())
            except Exception as e:
                pass

    return HttpResponse(json.dumps({'notification_infos': notification_infos}), 'application/json')


def check_notification(request, notification_id):
    if request.user.is_authenticated:
        try:
            notification_controller = NotificationController.objects.select_related(
                'replynotification__reply__post__board',
                'rereplynotification__rereply__post__board',
                'likenotification__like__post__board',
                'notification_type',
                'receiver',
                'sender',
            ).get(
                id=notification_id,
                receiver=request.user,
            )
        except NotificationController.DoesNotExist as e:
            raise Http404

        if not notification_controller.is_checked:
            with transaction.atomic():
                notification_controller.is_checked = True
                notification_controller.save(update_fields=["is_checked"])

                if request.user.receiver_profile.filter(is_checked=False).count() == 0:
                    request.user.has_notifications = False
                    request.user.save(update_fields=["has_notifications"])

        one_to_one_table = getattr(notification_controller, notification_controller.notification_type.name)

        # reply, rereply, like 중 하나
        lookup_model = getattr(one_to_one_table, notification_controller.notification_type.lookup_model)

        # 위치 가져오기
        post_id = lookup_model.post.id
        board_url = lookup_model.post.board.url

        # 최종 url 주소
        final_url = f"/{board_url}/{post_id}"

        # 만약 reply 면, 해당하는 댓글 # 로 보내기
        # 만약 rereply 면, 해당하는 대댓글 # 로 보내기
        if isinstance(lookup_model, Reply):
            final_url += f"#reply_{lookup_model.id}"
        elif isinstance(lookup_model, Rereply):
            final_url += f"#rereply_{lookup_model.id}"

        return redirect(f'{final_url}')
