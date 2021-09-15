from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
import re
from django.urls import reverse

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# 태그
class Tag(models.Model):
    tag_name = models.CharField(max_length=140, unique=True, db_index=True)

    def __str__(self):
        return self.tag_name

# 게시판 그룹
class BoardGroup(TimeStampedModel):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name

# 게시판
class Board(TimeStampedModel):
    url = models.SlugField(unique=True, db_index=True)
    name = models.CharField(max_length=30, unique=True, db_index=True)
    info = models.TextField(null=True, blank=True)
    board_img = models.ImageField(upload_to='board_img/', null=True, blank=True)
    board_group_id = models.ForeignKey(BoardGroup, on_delete=models.SET_NULL, null=True, blank=True)
    attribute = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.url

# 게시글
class Post(TimeStampedModel):
    title = models.CharField(max_length=150)
    body = RichTextUploadingField()
    def_tag = models.CharField(max_length=150, null=True, blank=True)
    post_img = models.ImageField(upload_to='post_img/', null=True, blank=True)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    tag_set = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title
    
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.def_tag)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(tag_name=t)
            self.tag_set.add(tag)

    def short_body(self):
        if len(self.body) > 200:
            return self.body[:200]
        else:
            return self.body

    # sitemap 생성하기 위해서 reverse 사용하여 해당 매개변수를 넣기
    def get_absolute_url(self):
        try:
            return reverse('board:post', kwargs={'pk': self.id, 'board_url': self.board_id.url})
        except:
            pass

    def save(self, *args, **kwargs):
        saved = super(Post, self).save(*args, **kwargs)
        # TAG 저장
        if self.def_tag:
            self.tag_save()
        return saved

# 좋아요
class Like(TimeStampedModel):
    post_id = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id

# 댓글
class Reply(TimeStampedModel):
    post_id = models.ForeignKey(Post, related_name='replys', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = models.TextField()

    def __str__(self):
        return self.body

# 답글
class Rereply(TimeStampedModel):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_id = models.ForeignKey(Reply, related_name='rereplys', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = models.TextField()

    def __str__(self):
        return self.body

    # 댓글의 post_id로 대댓글 post_id 저장
    def save(self, *args, **kwargs): 
        if self.reply_id:
            self.post_id = self.reply_id.post_id
        return super(Rereply, self).save(*args, **kwargs)

# URL 강조
class UrlImportant(TimeStampedModel):
    post_id = models.ForeignKey(Post, related_name='urlimportants', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url