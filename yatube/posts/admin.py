from django.contrib import admin

from .models import Post, Group, Follow, Comment


@admin.register(Follow)
@admin.register(Comment)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Администрационная панель к модели записей"""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date', 'group', 'author')
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Интерфейс администратора моделей сообщества"""
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    list_filter = ('title',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}
