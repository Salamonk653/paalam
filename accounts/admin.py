from django.contrib import admin
from .models import TemporaryBanIp, TemporaryBanIpAdmin

admin.site.register(TemporaryBanIp, TemporaryBanIpAdmin)