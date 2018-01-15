# -*- coding: utf-8 -*-
import json
from urllib.parse import urlparse

from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template.context_processors import csrf
from django.utils import timezone
from django.views import View

from accounts.models import TemporaryBanIp
from .special_func import get_next_url, get_client_ip


class ELoginView(View):
    # код метода get

    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу
            # с этим контекстом.
            # работает, как для url - /admin/login/ так и для /accounts/login/
            context = create_context_username_csrf(request)
            return render_to_response('accounts/login.html', context=context)

    def post(self, request):
        # забираем данные формы авторизации из запроса
        form = AuthenticationForm(request, data=request.POST)

        # забираем IP адрес из запроса
        ip = get_client_ip(request)
        # получаем или создаём новую запись об IP, с которого вводится пароль, на предмет блокировки
        obj, created = TemporaryBanIp.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )

        # если IP заблокирован и время разблокировки не настало
        if obj.status is True and obj.time_unblock > timezone.now():
            context = create_context_username_csrf(request)
            if obj.attempts == 3 or obj.attempts == 6:
                # то открываем страницу с сообщением о блокировки на 15 минут при 3 и 6 неудачных попытках входа
                return render_to_response('accounts/block_15_minutes.html', context=context)
            elif obj.attempts == 9:
                # или открываем страницу о блокировке на 24 часа, при 9 неудачных попытках входа
                return render_to_response('accounts/block_24_hours.html', context=context)
        elif obj.status is True and obj.time_unblock < timezone.now():
            # если IP заблокирован, но время разблокировки настало, то разблокируем IP
            obj.status = False
            obj.save()

        # если пользователь ввёл верные данные, то авторизуем его и удаляем запись о блокировке IP
        if form.is_valid():
            auth.login(request, form.get_user())
            obj.delete()

            next = urlparse(get_next_url(request)).path
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            return redirect(next)
        else:
            # иначе считаем попытки и устанавливаем время разблокировки и статус блокировки
            obj.attempts += 1
            if obj.attempts == 3 or obj.attempts == 6:
                obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
                obj.status = True
            elif obj.attempts == 9:
                obj.time_unblock = timezone.now() + timezone.timedelta(1)
                obj.status = True
            elif obj.attempts > 9:
                obj.attempts = 1
            obj.save()

        context = create_context_username_csrf(request)
        context['login_form'] = form

        return render_to_response('accounts/login.html', context=context)


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = AuthenticationForm
    return context


class BookmarkView(View):
    # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
    model = None

    def post(self, request, pk):
        # нам потребуется пользователь
        user = auth.get_user(request)
        # пытаемся получить закладку из таблицы, или создать новую
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        # если не была создана новая закладка,
        # то считаем, что запрос был на удаление закладки
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
