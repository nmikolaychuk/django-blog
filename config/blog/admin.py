from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Панель администрирования постов."""
    list_display = ['title', 'slug', 'author', 'published', 'status']
    list_filter = ['status', 'created', 'published', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published'
    ordering = ['status', 'published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Панель администрирования комментариев к постам."""
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['name', 'created', 'active', 'updated']
    search_fields = ['name', 'email', 'body']
    raw_id_fields = ['post']
