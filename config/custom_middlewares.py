import datetime

from django.db import transaction

from common_library import get_client_ip, time_until_end_of_day
from control.models import IPVisitant, TodayYesterday


class VisitorCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 최초 설정 및 초기화

    def __call__(self, request):
        # 뷰가 호출되기 전에 실행될 코드들
        client_ip = get_client_ip(request)

        response = self.get_response(request)

        # 방문한 적이 없을 경우 (쿠키)
        if not self.is_cookie_visited(request):
            self.set_cookie_visited(response)

            # 방문한 적이 없을 경우 (테이블)
            if not self.is_table_visited(client_ip):
                with transaction.atomic():
                    self.set_table_visited(client_ip)
                    self.update_today_visitor()

        return response

    @staticmethod
    def is_cookie_visited(request):
        return request.COOKIES.get('is_visited')

    @staticmethod
    def set_cookie_visited(response):
        end_of_day_left_time = time_until_end_of_day()
        response.set_cookie('is_visited', 1, max_age=end_of_day_left_time)

    @staticmethod
    def is_table_visited(client_ip):
        today_filter_options = {
            "created_at__year": datetime.date.today().year,
            "created_at__month": datetime.date.today().month,
            "created_at__day": datetime.date.today().day,
        }
        if IPVisitant.objects.filter(ip=client_ip, **today_filter_options).exists():
            return True
        return False

    @staticmethod
    def set_table_visited(client_ip):
        IPVisitant.objects.create(
                ip=client_ip
        )

    def update_today_visitor(self):
        visitor_info = TodayYesterday.objects.last()
        if visitor_info:
            visitor_info.today = self.count_today_visitor()
            visitor_info.save(update_fields=['today'])
        else:
            TodayYesterday.objects.create(
                today=0,
                yesterday=0,
            )

    @staticmethod
    def count_today_visitor():
        today_filter_options = {
            "created_at__year": datetime.date.today().year,
            "created_at__month": datetime.date.today().month,
            "created_at__day": datetime.date.today().day,
        }
        today_visitor_count = IPVisitant.objects.filter(
            **today_filter_options
        ).count()
        return today_visitor_count


