from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Reply)
admin.site.register(Rereply)
admin.site.register(Tag)
admin.site.register(UrlImportant)
admin.site.register(BoardGroup)