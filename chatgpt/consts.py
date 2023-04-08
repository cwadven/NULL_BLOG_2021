from config.enums import StrValueLabel
from django.conf import settings


CHATGPT_URL = 'https://api.openai.com/v1/chat/completions'
CHATGPT_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {settings.CHATGPT_KEY}'
}


class LessonSummary(StrValueLabel):
    PYTHON_TIP = ('Python Tip', '파이썬 꿀팁')
