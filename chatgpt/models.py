from django.db import models


class LessonInformation(models.Model):
    """
    ChatGPT 질문지
    tag 를 작성하면 tag 로 작성한 답변 히스토리를 가지고 지금까지 정보를 기반으로 이야기
    """
    summary = models.TextField(null=True, blank=True, help_text='요약')
    system_prompt = models.CharField(max_length=45, null=True, blank=True, help_text='시스템 프롬프트')
    prompt = models.TextField(help_text='프롬프트')
    tag = models.CharField(max_length=45, null=True, blank=True, help_text='태그')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ChatGPT 질문지'
        verbose_name_plural = 'ChatGPT 질문지'


class Lesson(models.Model):
    summary = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=45, null=True, blank=True, db_index=True, help_text='태그')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ChatGPT 응답 마지막 결과'
        verbose_name_plural = 'ChatGPT 응답 마지막 결과'

    def __str__(self):
        return f'{self.id} {self.body[:10] + "..." if len(self.body) > 10 else self.body}'

    @staticmethod
    def request_lesson_to_chatgpt_system_prompt():
        return '너는 Python 시니어 개발자'

    @staticmethod
    def request_lesson_to_chatgpt():
        return '이전까지 알려준 꿀팁 제외하고,' \
               ' 파이썬 3.7 이상 버전 꿀팁 코드를 최대 3개만 알려줘' \
               ' 예제 코드까지 작성해줘'
