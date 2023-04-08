from django.db import migrations


def forward(apps, schema_editor):
    LessonInformation = apps.get_model('chatgpt', 'LessonInformation')
    LessonInformation.objects.get_or_create(
        summary='Python Tip',
        system_prompt='너는 Python 시니어 개발자',
        prompt='이전까지 알려준 꿀팁 제외하고, 파이썬 3.7 이상 버전 꿀팁 코드를 최대 3개만 알려줘 예제 코드까지 작성해줘',
        tag='python',
    )


def backward(apps, schema_editor):
    LessonInformation = apps.get_model('chatgpt', 'LessonInformation')
    LessonInformation.objects.filter(
        summary='Python Tip',
        system_prompt='너는 Python 시니어 개발자',
        prompt='이전까지 알려준 꿀팁 제외하고, 파이썬 3.7 이상 버전 꿀팁 코드를 최대 3개만 알려줘 예제 코드까지 작성해줘',
        tag='python',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt', '0003_auto_20230408_1544'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
