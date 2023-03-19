from django.contrib import admin

from chatgpt.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'summary',
        'body',
    )
