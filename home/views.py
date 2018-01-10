from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views import View
from django.views.generic import ListView

from home.forms import PostForm, CommentForm
from home.models import *


# class PostsListView(ListView):  # представление в виде списка
#     model = Post  # модель для представления


# class PostDetailView(DetailView):  # детализированное представление модели
#     model = Post

# def category(request):
#     context ={}
#     context['category'] = Category.objects.all()
#     return render(request, 'base.html', context)


class home(ListView):
    template_name = 'base.html'
    queryset = Post.objects.filter(active=True).order_by('-id')
    paginate_by = 12


class psychology(ListView):
    template_name = 'psychology.html'
    queryset = Post.objects.filter(category__name='психология')
    paginate_by = 12


class health(ListView):
    template_name = 'health.html'
    queryset = Post.objects.filter(category__name='ден-соолук')
    paginate_by = 12


class family(ListView):
    template_name = 'family.html'
    queryset = Post.objects.filter(category__name='үй-бүлө')
    paginate_by = 12
    # context_object_name = 'family'


def post_single(request, id):
    form = CommentForm

    post = get_object_or_404(Post, id=id)
    comment = Comment.objects.filter(post=post)
    category = Category.objects.all()
    return render(request, 'home/post_detail.html',
                  {'post': post, 'form': form, 'comment': comment, 'category': category})


#
#
def addcomment(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, id=id)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.post = post
            form.save()
        return HttpResponseRedirect(post.get_absolute_url())


def post_new(request):
    form = PostForm()
    context = {}
    context['category'] = Category.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST)
        context['form'] = form
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # post.created = timezone.now()
            form.save()
            return redirect('/')
    return render(request, 'post_edit.html', context)


def post_edit(request, id):
    context = {}
    context['category'] = Category.objects.all()
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        context['form'] = form
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created = timezone.now()
            post.save()
            return redirect('/post/%s' % id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', context)


def post_delete(request, id):
    Post.objects.filter(id=id).delete()
    return redirect('/')


class EPostView(View):
    template_name = 'index.html'  # Шаблон статьи

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)  # Забираем статью из базы данных
        context = {}

        # Далее забираем объект сегодняшней статистики или создаём новый, если требуется
        obj, created = PostStatistic.objects.get_or_create(
            defaults={
                "post": post,
                "created": timezone.now()
            },
            # При этом определяем, забор объекта статистики или его создание
            # по двум полям: дата и внешний ключ на статью
            created=timezone.now(), post=post
        )
        obj.views += 1  # инкрементируем счётчик просмотров и обновляем поле в базе данных
        obj.save(update_fields=['views'])

        # А теперь забираем список 5 последний самых популярных статей за неделю
        popular = PostStatistic.objects.filter(
            # отфильтровываем записи за последние 7 дней
            created__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
        ).values(
            # Забираем интересующие нас поля, а именно id и заголовок
            # К сожалению забрать объект по внешнему ключу в данном случае не получится
            # Только конкретные поля из объекта
            'post_id', 'post__title'
        ).annotate(
            # Суммируем записи по просмотрам
            # Всё суммируется корректно с соответствием по запрашиваемым полям объектов 
            views=Sum('views')
        ).order_by(
            # отсортируем записи по убыванию
            '-views')[:5]  # Заберём последние пять записей

        context['popular_list'] = popular  # Отправим в контекст список статей

        return render_to_response(template_name=self.template_name, context=context)
