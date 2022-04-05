from django.db import models


class PostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def active(self):
        return self.filter(is_active=True)
