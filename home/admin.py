from django.contrib import admin

from home.models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(Category)
admin.site.register(PostStatistic,PostStatisticAdmin)