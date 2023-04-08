from django.contrib import admin

from chatgpt.models import Lesson, LessonInformation


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'summary',
        'body',
    )


@admin.register(LessonInformation)
class LessonInformationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'summary',
        'system_prompt',
        'prompt',
        'tag',
    )
