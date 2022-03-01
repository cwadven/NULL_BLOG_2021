import datetime

from django.db.models import F

from control.models import TodayYesterday, IPVisitant


def update_yesterday_and_today_visitor():
    visitor_info_set = TodayYesterday.objects.all()

    if visitor_info_set.exists():
        visitor_info_set.update(
            yesterday=F('today'),
            today=0,
        )
        print("updated")
        visitor_info = TodayYesterday.objects.all()[0]

        if visitor_info.yesterday == 0:
            print("yesterday was 0")
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            visitor_info.yesterday = IPVisitant.objects.filter(created_at__gt=yesterday).count()
            visitor_info.save(update_fields=['yesterday'])

        print("ended")
