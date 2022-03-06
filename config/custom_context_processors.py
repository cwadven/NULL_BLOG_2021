from control.models import TodayYesterday


def visitor_info(request):
    _visitor_info = {
        "today": 0,
        "yesterday": 0,
    }

    day_visitor_info = TodayYesterday.objects.last()

    if day_visitor_info:
        _visitor_info = day_visitor_info

    return {'visitor_info': _visitor_info}
