from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import ELoginView

urlpatterns = [
    url(r'^admin/login/', ELoginView.as_view()),
    url(r'^', include('home.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('accounts.urls')),
              ]+ \
              static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)