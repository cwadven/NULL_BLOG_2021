import datetime
import re

from django.core.paginator import Paginator


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def time_until_end_of_day(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)


def web_paging(request, queryset, post_size=10, page_num_size=5):
    """
    request: http request
    queryset: Model Queryset
    post_size: 1 page post 개수
    page_num_size: 페이지네이션 번호 보여질 개수 (1,2,3,4: 4개 / 1,2,3: 3개)
    return: page_posts(paginator_queryset) / page_range(number_range)
    """
    page = request.GET.get('page', 1)
    posts = Paginator(queryset, post_size)

    max_index = len(posts.page_range)

    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_num_size) * page_num_size
    end_index = start_index + page_num_size

    if end_index >= max_index:
        end_index = max_index

    page_range = posts.page_range[start_index:end_index]

    page_posts = posts.get_page(page)  # 페이지네이션 만들기

    return {
        "page_posts": page_posts,
        "page_range": page_range,
    }


def transition_special_code(special_code: str) -> str:
    SPECIAL_CHAR = {
        "&gt;": ">",
        "&nbsp;": " ",
        "&lt;": "<",
        "&amp;": "&",
        "&quot;": '"',
        "&minus;": "-",
    }
    special_code = re.sub('<[^<]+?>', '', special_code)
    return SPECIAL_CHAR.get(special_code, special_code)
