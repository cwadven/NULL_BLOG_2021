from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# 태그
class Announce(TimeStampedModel):
    title = models.CharField(max_length=140)
    body = models.TextField()

    class Meta:
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항"

    def __str__(self):
        return self.title


# 모든 방문자 IP
class IPVisitant(models.Model):
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "방문자 IP"
        verbose_name_plural = "방문자 IP"

    def __str__(self):
        return f'{self.ip} {self.created_at}'


# 방문자 수, 조회 테이블
# 쿠키가 없을 때, 이 테이블을 기준으로 TodayYesterday 테이블 Today 최신화
# [Cron]
class TodayYesterday(models.Model):
    today = models.PositiveIntegerField(default=0)
    yesterday = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "방문자 수"
        verbose_name_plural = "방문자 수"

    def __str__(self):
        return f'[{self.created_at}] Today: {self.today} / Yesterday: {self.yesterday}'
