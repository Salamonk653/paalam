from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone
from uuslug import uuslug


class Category(models.Model):
    class Meta:
        db_table = u'Category'
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    name = models.CharField('Имя', max_length=80, blank=True, null=True, default=None)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class HashTag(models.Model):
    class Meta():
        db_table = 'Tags'
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'

    name = models.CharField(u"Имя", max_length=50, unique=True)

    # post = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Post(models.Model):
    class Meta:
        db_table = u'Статьи'

    user = models.ForeignKey(User, verbose_name=u'Пользователь', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=u'Категория', on_delete=models.CASCADE, blank=True, null=True,
                                 default=None)
    slug = models.CharField(verbose_name=u'Транслит', max_length=200, blank=True)
    image = models.ImageField("Изоброжение", upload_to='post/', blank=True)
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст статьи')
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
        verbose_name_plural = u'Комментарии'
        verbose_name = u'Комментарий'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(verbose_name=u'Комментарий')
    created = models.DateTimeField(auto_now_add=True)


class PostStatistic(models.Model):
    class Meta:
        db_table = "ArticleStatistic"

    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # внешний ключ на статью
    created = models.DateField(u'Дата', default=timezone.now)  # дата
    views = models.IntegerField(u'Просмотры', default=0)  # количество просмотров в эту дату

    def __str__(self):
        return self.post.title


class PostStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'views')  # отображаемые поля в админке
    search_fields = ('__str__',)
