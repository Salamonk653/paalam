# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PostBase(models.Model):
    class Meta:
        abstract = True  # данное поле указывает, что класс абстрактный
        # и что для него не нужно создавать таблицу

    SPAM = 'S'
    NOT_MODERATED = 'N'
    POST_MODERATED = 'P'
    MODERATED = 'M'
    MODERATION_CHOICES = (
        (SPAM, 'SPAM'),
        (NOT_MODERATED, 'Not Moderated'),
        (POST_MODERATED, 'Post Moderated'),
        (MODERATED, 'Moderated')
    )

    author = models.ForeignKey(User, verbose_name=_(u"Автор"))
    content = models.TextField(_(u'Содержание'), blank=True)
    pub_date = models.DateTimeField(_(u'Дата публикации'), blank=True, null=True)
    moderation = models.CharField(
        _(u'Модерация'),
        max_length=1,
        choices=MODERATION_CHOICES,
        default=NOT_MODERATED
    )


class BookmarkBase(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, verbose_name="Пользователь")

    def __str__(self):
        return self.user.username