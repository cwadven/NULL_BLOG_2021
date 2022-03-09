from django.contrib import admin
from .models import *


class RereplyInline(admin.TabularInline):
    model = Rereply


class ReplyInline(admin.TabularInline):
    inlines = [
        RereplyInline
    ]
    model = Reply


class LikeInline(admin.TabularInline):
    model = Like


class UrlImportantInline(admin.TabularInline):
    model = UrlImportant


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'url',
        'name',
        'info',
        'attribute',
        'board_group_name',
    )

    def board_group_name(self, obj):
        if obj.board_group:
            return obj.board_group.group_name
        return None


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        UrlImportantInline,
        ReplyInline,
        LikeInline,
    ]

    list_display = (
        'id',
        'author',
        'board_name',
        'title',
        '_tag_set'
    )

    def board_name(self, obj):
        if obj.board:
            return obj.board.name
        return None

    def author(self, obj):
        if obj.author:
            return obj.author.nickname
        return None

    def _tag_set(self, obj):
        if obj.tag_set.exists():
            return ", ".join([tag.tag_name for tag in obj.tag_set.all()])
        return None


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tag_name',
    )
    list_editable = [
        'tag_name',
    ]


@admin.register(BoardGroup)
class BoardGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group_name',
    )
    list_editable = [
        'group_name',
    ]
