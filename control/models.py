from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# 태그
class Announce(TimeStampedModel):
    title = models.CharField(max_length=140)
    body = models.TextField()

    def __str__(self):
        return self.title