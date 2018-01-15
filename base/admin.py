from django.contrib import admin

from base.models import PostBase


class PostBaseAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'pub_date')
    search_fields = ('content', 'author__username')
    list_filter = ('moderation',)
    actions = ['make_spam', 'make_not_moderated', 'make_post_moderated', 'make_moderated']

    def moderate(self, request, rows_updated, choice_description):
        if rows_updated == 1:
            message_bit = "1 запись помечена, как %s" % choice_description
        else:
            message_bit = "%s записей отмечены, как %s." % (rows_updated, choice_description)
        self.message_user(request, "%s" % message_bit)

    def make_spam(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=PostBase.SPAM),
            choice_description="SPAM"
        )

    make_spam.short_description = "Отметить помеченные, как SPAM"

    def make_not_moderated(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=PostBase.NOT_MODERATED),
            choice_description="NOT_MODERATED"
        )

    make_not_moderated.short_description = "Отметить помеченные, как NOT_MODERATED"

    def make_post_moderated(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=PostBase.POST_MODERATED),
            choice_description="POST_MODERATED"
        )

    make_post_moderated.short_description = "Отметить помеченные, как POST_MODERATED"

    def make_moderated(self, request, queryset):
        self.moderate(
            request=request,
            rows_updated=queryset.update(moderation=PostBase.MODERATED),
            choice_description="MODERATED"
        )

    make_moderated.short_description = "Отметить помеченные, как MODERATED"
