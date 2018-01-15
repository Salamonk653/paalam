from django.db import models
from django.contrib import admin

from base.models import BookmarkBase
from home.models import *


class TemporaryBanIp(models.Model):
    class Meta:
        db_table = "TemporaryBanIp"

    ip_address = models.GenericIPAddressField(u"IP адрес")
    attempts = models.IntegerField(u"Неудачных попыток", default=0)
    time_unblock = models.DateTimeField(u"Время разблокировки", blank=True)
    status = models.BooleanField(u"Статус блокировки", default=False)

    def __str__(self):
        return self.ip_address


class TemporaryBanIpAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'status', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)


class BookmarkArticle(BookmarkBase):
    class Meta:
        db_table = "bookmark_article"

    obj = models.ForeignKey(Post, verbose_name="Статья")


class BookmarkComment(BookmarkBase):
    class Meta:
        db_table = "bookmark_comment"

    obj = models.ForeignKey(Comment, verbose_name="Комментарий")