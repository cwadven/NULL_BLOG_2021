from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.conf import settings
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    user_img = models.ImageField(upload_to='user_img/', null=True, blank=True)

    def __str__(self):
        return '%s' % (self.username)

    #저장할때 이미지는 orientation 맞춰서 저장 또한 전부 삭제 exif정보
    def save(self, *args, **kwargs): 
        if self.user_img:
            pilImage = Img.open(BytesIO(self.user_img.read()))
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(pilImage._getexif().items())

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)

                output = BytesIO()
                pilImage.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.user_img = File(output, self.user_img.name)
            except:
                pass

        return super(User, self).save(*args, **kwargs)

from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount
from django.db import transaction

# 네이버로 가입한 계정에 사용자 이름을 추가
def receiver_social_signup(sender, instance, created, *args, **kwargs):
    # Email이 생성됐을 경우
    if created:
        # 이름을 구한다 (토큰에 이름이 있다 하지만 User 테이블에 바로 생성 될 떄는 잡히지 않는다)
        # 그래서 Email이 생성 됐을 때 실행 했다.
        social_info = instance.user.socialaccount_set.all()[0]
        user = User.objects.get(id=instance.user.id)
        
        # 트랜잭션
        with transaction.atomic():
            # 네이버일 경우
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
# Sender
post_save.connect(receiver_social_signup, sender=SocialAccount)