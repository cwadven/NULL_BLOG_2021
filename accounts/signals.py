import logging
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount

from accounts.models import User, UserProvider


logger = logging.getLogger('django')


@receiver(post_save, sender=SocialAccount)
def receiver_social_signup(sender, instance, created, *args, **kwargs):
    if created:
        social_info = instance.user.socialaccount_set.all()[0]
        user = User.objects.get(id=instance.user.id)

        with transaction.atomic():
            provider = None

            try:
                provider = UserProvider.objects.get(
                    name=social_info.provider,
                )
            except UserProvider.DoesNotExist as e:
                logger.error(e)

            if social_info.provider == 'naver':
                user.provider = provider
                user.username = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.save()
            elif social_info.provider == 'google':
                user.provider = provider
                user.username = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['name'] + str(social_info.extra_data['id'])[:5]
                user.save()
            elif social_info.provider == 'kakao':
                user.provider = provider
                user.username = social_info.extra_data['properties']['nickname'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['properties']['nickname'] + str(social_info.extra_data['id'])[:5]
                user.save()
            elif social_info.provider == 'github':
                user.provider = provider
                user.username = social_info.extra_data['login'] + str(social_info.extra_data['id'])[:5]
                user.nickname = social_info.extra_data['login'] + str(social_info.extra_data['id'])[:5]
                user.save()
