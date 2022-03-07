from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount

from accounts.models import User


@receiver(post_save, sender=SocialAccount)
def receiver_social_signup(sender, instance, created, *args, **kwargs):
    if created:
        social_info = instance.user.socialaccount_set.all()[0]
        user = User.objects.get(id=instance.user.id)

        with transaction.atomic():
            if social_info.provider == 'naver':
                user.username = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.save()
            elif social_info.provider == 'google':
                user.username = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.save()
            elif social_info.provider == 'kakao':
                user.username = social_info.extra_data['properties']['nickname'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['properties']['nickname'] + str(social_info.extra_data['id'])[:5]
                user.save()
            elif social_info.provider == 'github':
                user.username = social_info.extra_data['login'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['login'] + str(social_info.extra_data['id'])[:5]
                user.save()
