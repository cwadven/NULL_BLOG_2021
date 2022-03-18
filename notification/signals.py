from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from board.models import Reply, Rereply, Like
from notification.models import (
    NotificationController,
    ReplyNotification, RereplyNotification, LikeNotification
)


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
            instance.post.author.has_notification = True
            instance.post.author.save(update_fields=["has_notification"])


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
            instance.reply.author.has_notification = True
            instance.reply.author.save(update_fields=["has_notification"])


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
            instance.post.author.has_notification = True
            instance.post.author.save(update_fields=["has_notification"])

