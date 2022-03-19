from django.db import models

from accounts.models import User
from board.models import Reply, Rereply, Like


class NotificationType(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    lookup_model = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "알림 타입"
        verbose_name_plural = "알림 타입"

    def __str__(self):
        return f'{self.name}'


class NotificationController(models.Model):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender_profile")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="receiver_profile")
    representative_message = models.TextField()
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "알림 중재자"
        verbose_name_plural = "알림 중재자"

    def __str__(self):
        return f'[{self.notification_type.name}] {self.id}'


class ReplyNotification(models.Model):
    notification_controller = models.OneToOneField(NotificationController, on_delete=models.CASCADE)
    reply = models.OneToOneField(Reply, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "댓글 알림"
        verbose_name_plural = "댓글 알림"

    def __str__(self):
        return f'{self.id} notification_controller_id: {self.notification_controller.notification_type.name}/reply_id: {self.reply_id}'

    def get_custom_response(self):
        # 게시글에 댓글
        title = f'{self.reply.post.title} 에 댓글을 작성했습니다.'
        content = f'{self.reply.body}'
        sender = f'{self.notification_controller.sender}'

        return title, content, sender

    def get_ajax_notification_response(self):
        return {
            "id": self.notification_controller.id,
            "notification_type": self.notification_controller.notification_type.name,
            "title": "<span>[ 댓글 ]</span>",
            "body": self.reply.body,
            "sender": self.notification_controller.sender.nickname,
        }


class RereplyNotification(models.Model):
    notification_controller = models.OneToOneField(NotificationController, on_delete=models.CASCADE)
    rereply = models.OneToOneField(Rereply, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "대댓글 알림"
        verbose_name_plural = "대댓글 알림"

    def __str__(self):
        return f'{self.id} notification_controller_id: {self.notification_controller.notification_type.name}/rereply_id: {self.rereply_id}'

    def get_custom_response(self):
        # 게시글에 대댓글
        title = f'{self.rereply.reply.body} 에 답글을 작성했습니다.'
        content = f'{self.rereply.body}'
        sender = f'{self.notification_controller.sender}'

        return title, content, sender

    def get_ajax_notification_response(self):
        return {
            "id": self.notification_controller.id,
            "notification_type": self.notification_controller.notification_type.name,
            "title": "<span>[ 답글 ]</span>",
            "body": self.rereply.body,
            "sender": self.notification_controller.sender.nickname,
        }


class LikeNotification(models.Model):
    notification_controller = models.OneToOneField(NotificationController, on_delete=models.CASCADE)
    like = models.OneToOneField(Like, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "좋아요 알림"
        verbose_name_plural = "좋아요 알림"

    def __str__(self):
        return f'{self.id} notification_controller_id: {self.notification_controller.notification_type.name}/like_id: {self.like_id}'

    def get_custom_response(self):
        # 게시글에 좋아요
        title = f'{self.like.post.title} 에 좋아요를 했습니다.'
        content = f''
        sender = f'{self.notification_controller.sender}'

        return title, content, sender

    def get_ajax_notification_response(self):
        return {
            "id": self.notification_controller.id,
            "notification_type": self.notification_controller.notification_type.name,
            "title": "<span>[ 좋아요 ]</span>",
            "body": f"게시글 '{self.like.post.title[:10] + '...' if len(self.like.post.title) > 10 else self.like.post.title}' 에 좋아요를 했습니다.",
            "sender": self.notification_controller.sender.nickname,
        }
