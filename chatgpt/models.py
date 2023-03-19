from django.db import models


class Lesson(models.Model):
    summary = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ChatGPT 교훈"
        verbose_name_plural = "ChatGPT 교훈"

    def __str__(self):
        return f'{self.id} {self.body[:10] + "..." if len(self.body) > 10 else self.body}'

    @staticmethod
    def request_lesson_to_chatgpt():
        return '교훈이 될 수 있는 좋은 말해줘'

    @classmethod
    def request_lesson_summary_by_body(cls, body):
        return f'{body} 를 1줄로 전부 요약해줘'
