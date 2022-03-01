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

    def __str__(self):
        return self.title


# 모든 방문자 IP
class IPVisitant(models.Model):
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip} {self.created_at}'


# 방문자 수, 조회 테이블
# 쿠키가 없을 때, 이 테이블을 기준으로 TodayYesterday 테이블 Today 최신화
# [Cron]
# 하루 지나면 yesterday 는 today 값으로 변경, today 는 0 으로 초기화
# 만약 yesterday 가 0 일 경우, 00:00 시에 들어오는 유저로 today 가 바로 0 으로 바뀌는 상황을 대비해 한번 어제 값 조회
class TodayYesterday(models.Model):
    today = models.PositiveIntegerField(default=0)
    yesterday = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'today: {self.today} yesterday: {self.yesterday}'


