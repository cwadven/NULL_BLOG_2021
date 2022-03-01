from control.models import TodayYesterday


def visitor_info(request):
    _visitor_info = {
        "today": 0,
        "yesterday": 0,
    }

    visitor_info_set = TodayYesterday.objects.all()

    if visitor_info_set.exists():
        _visitor_info = visitor_info_set.values()[0]

    return {'visitor_info': _visitor_info}
