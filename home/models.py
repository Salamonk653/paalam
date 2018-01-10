from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone
from uuslug import uuslug


class Category(models.Model):
    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField('Имя', max_length=80, blank=True, null=True, default=None)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class HashTag(models.Model):
    class Meta():
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField("Имя", max_length=50, unique=True)

    # post = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Post(models.Model):
    class Meta:
        db_table = 'Статьи'

    user = models.ForeignKey(User, verbose_name='Пользователь')
    category = models.ForeignKey(Category, verbose_name='Категория', blank=True, null=True, default=None)
    slug = models.CharField(verbose_name='Транслит', max_length=200, blank=True)
    image = models.ImageField("Изоброжение", upload_to='post/', blank=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст статьи')
    hash_tag = models.ManyToManyField(HashTag)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/post/%s/" % self.id

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Post, self).delete(*args, **kwargs)


class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)


class PostStatistic(models.Model):
    class Meta:
        db_table = "ArticleStatistic"

    post = models.ForeignKey(Post)  # внешний ключ на статью
    created = models.DateField('Дата', default=timezone.now)  # дата
    views = models.IntegerField('Просмотры', default=0)  # количество просмотров в эту дату

    def __str__(self):
        return self.post.title


class PostStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'views')  # отображаемые поля в админке
    search_fields = ('__str__',)
