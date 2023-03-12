from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from board.models import Reply, Rereply, Like
from common_conts import REPLY_NOTIFICATION, EMAIL_TEMPLATE_MAPPER, REREPLY_NOTIFICATION, LIKE_NOTIFICATION
from notification.models import (
    NotificationController,
    ReplyNotification, RereplyNotification, LikeNotification
)
from notification.task import send_email_async_notification


@receiver(post_save, sender=Reply)
def reply_post(sender, instance, *args, **kwargs):
    if instance.author_id != instance.post.author_id:
        with transaction.atomic():
            notification_controller = NotificationController.objects.create(
                notification_type_id=1,
                sender=instance.author,
                receiver=instance.post.author,
                representative_message=f"댓글을 작성했습니다.",
            )
            ReplyNotification.objects.create(
                notification_controller=notification_controller,
                reply=instance,
            )
            instance.post.author.has_notifications = True
            instance.post.author.save(update_fields=["has_notifications"])
        if instance.post.author.email:
            send_email_async_notification.apply_async(
                (
                    f'[Nulls 블로그] {instance.post.title[:20]} 게시글에 댓글이 달렸습니다.',
                    EMAIL_TEMPLATE_MAPPER[REPLY_NOTIFICATION],
                    {
                        'post_title': f'{instance.post.title} 에 댓글이 달렸습니다.',
                        'post_url': 'https://nulls.co.kr' + instance.post.get_absolute_url() + '#reply_' + str(instance.id),
                        'reply_nickname': instance.author.nickname,
                        'reply_body': instance.body,
                    },
                    [instance.post.author.email],
                )
            )


@receiver(post_save, sender=Rereply)
def rereply_post(sender, instance, *args, **kwargs):
    if instance.author_id != instance.reply.author_id:
        with transaction.atomic():
            notification_controller = NotificationController.objects.create(
                notification_type_id=2,
                sender=instance.author,
                receiver=instance.reply.author,
                representative_message=f"대댓글을 작성했습니다.",
            )
            RereplyNotification.objects.create(
                notification_controller=notification_controller,
                rereply=instance,
            )
            instance.reply.author.has_notifications = True
            instance.reply.author.save(update_fields=["has_notifications"])
        if instance.reply.author.email:
            send_email_async_notification.apply_async(
                (
                    f'[Nulls 블로그] 댓글에 대댓글이 달렸습니다.',
                    EMAIL_TEMPLATE_MAPPER[REREPLY_NOTIFICATION],
                    {
                        'information': f'{instance.reply.author.nickname} 님의 댓글에 대댓글이 달렸습니다.',
                        'post_url': 'https://nulls.co.kr' + instance.post.get_absolute_url() + '#rereply_' + str(instance.id),
                        'rereply_nickname': instance.author.nickname,
                        'rereply_body': instance.body,
                    },
                    [instance.reply.author.email]
                )
            )


@receiver(post_save, sender=Like)
def like_post(sender, instance, *args, **kwargs):
    if instance.author_id != instance.post.author_id:
        with transaction.atomic():
            notification_controller = NotificationController.objects.create(
                notification_type_id=3,
                sender=instance.author,
                receiver=instance.post.author,
                representative_message=f"좋아요를 했습니다.",
            )
            LikeNotification.objects.create(
                notification_controller=notification_controller,
                like=instance,
            )
            instance.post.author.has_notifications = True
            instance.post.author.save(update_fields=["has_notifications"])
        if instance.post.author.email:
            send_email_async_notification.apply_async(
                (
                    f'[Nulls 블로그] 게시글에 좋아요가 달렸습니다.',
                    EMAIL_TEMPLATE_MAPPER[LIKE_NOTIFICATION],
                    {
                        'post_title': f'{instance.post.title} 게시글에 좋아요가 달렸습니다.',
                        'post_url': 'https://nulls.co.kr' + instance.post.get_absolute_url(),
                        'liker_nickname': instance.author.nickname,
                    },
                    [instance.post.author.email]
                )
            )
