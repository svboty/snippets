from django.contrib import admin
from MainApp.models import Snippet, Comment

# Register your models here.


class CommentAdmin(admin.TabularInline):
    model = Comment
    fields = ('author', 'text', )
    raw_id_fields = ('author', )
    extra = 0


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    inlines = (CommentAdmin, )
    list_display = ('name', 'lang', 'user_name')

    def user_name(self, instance):
        return instance.user.username if instance.user else 'Anonymous'
