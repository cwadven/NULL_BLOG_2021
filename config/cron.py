import datetime
from control.models import TodayYesterday, IPVisitant


def update_yesterday_and_today_visitor():
    """
    하루에 한번씩 TodayYesterday 데이터 추가
    """
    yesterday_visitor_info = TodayYesterday.objects.all().last()

    if yesterday_visitor_info:
        print("----created----")
        TodayYesterday.objects.create(
            yesterday=yesterday_visitor_info.today,
            today=0,
        )
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_info = {
            "created_at__year": yesterday.year,
            "created_at__month": yesterday.month,
            "created_at__day": yesterday.day,
        }
        yesterday_date = f"{yesterday_info['created_at__year']}" + "-" + f"{yesterday_info['created_at__month']:02}" + "-" + f"{yesterday_info['created_at__day']:02}"

        print(f"[{yesterday_date}] Yesterday check with before TodayYesterday Field: {yesterday_visitor_info.today}")
        print(f"[{yesterday_date}] Yesterday check with IPVisitant Row Count: {IPVisitant.objects.filter(**yesterday_info).count()}")
        print("-----ended-----")
    else:
        TodayYesterday.objects.create(
            yesterday=0,
            today=0,
        )
