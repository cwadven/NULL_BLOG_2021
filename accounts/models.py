from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO

from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProvider(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "가입유형"
        verbose_name_plural = "가입유형"

    def __str__(self):
        return '%s' % self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    provider = models.ForeignKey(UserProvider, on_delete=models.SET_NULL, null=True, blank=True)
    user_img = models.ImageField(upload_to='user_img/', null=True, blank=True)
    has_notifications = models.BooleanField(default=False)

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

    def __str__(self):
        return '%s' % self.username

    # 저장할때 이미지는 orientation 맞춰서 저장 또한 전부 삭제 exif 정보
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
