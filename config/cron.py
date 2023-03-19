import os
import pymysql
import datetime

from django.conf import settings

from chatgpt.models import Lesson
from chatgpt.services import get_chatgpt_response
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
            today=1,
        )


def database_backup():
    """
    데이터 베이스 백업
    """
    HOST = settings.DATABASES['default']['HOST']
    NAME = settings.DATABASES['default']['NAME']
    USER = settings.DATABASES['default']['USER']
    PASSWORD = settings.DATABASES['default']['PASSWORD']

    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=NAME,
        charset='utf8'
    )

    backup_path = '/var/www/backup'
    backup_file_name = f'nully_blog_{datetime.date.today().strftime("%Y-%m-%d")}.sql'
    os.system(
        f'mysqldump -h {HOST} -u {USER} -p{PASSWORD} {NAME} > {backup_path}/{backup_file_name}')

    conn.close()


def get_chatgpt_lesson():
    """
    ChatGPT로부터 교훈을 받아온다.
    """
    print("----request----")
    lesson = get_chatgpt_response(Lesson.request_lesson_to_chatgpt())
    if lesson:
        summary = get_chatgpt_response(Lesson.request_lesson_summary_by_body(lesson))

        if summary:
            Lesson.objects.create(
                body=lesson,
                summary=summary,
            )
            print("----created----")
    else:
        print("----failed----")
    print("-----ended-----")
