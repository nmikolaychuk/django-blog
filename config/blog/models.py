from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


TEXT_FIELD_MAX_LENGTH = 250
NAME_FIELD_MAX_LENGTH = 80
STATUS_FIELD_MAX_LENGTH = 2


class PublishedManager(models.Manager):
    """Модельный менеджер для извлечения опубликованных постов."""
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Пост блога."""
    class Status(models.TextChoices):
        """Статус поста."""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH, verbose_name='Title')
    slug = models.SlugField(max_length=TEXT_FIELD_MAX_LENGTH, unique_for_date='published', verbose_name='Slug')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Author')
    body = models.TextField(verbose_name='Post content')
    published = models.DateTimeField(default=timezone.now, verbose_name='Published datetime')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created datetime')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated datetime')
    status = models.CharField(
        max_length=STATUS_FIELD_MAX_LENGTH,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Post status'
    )
    objects = models.Manager()
    published_posts = PublishedManager()

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Получить канонический URL-адрес объекта."""
        return reverse(
            viewname='blog:post_detail',
            args=[
                self.published.year,
                self.published.month,
                self.published.day,
                self.slug,
            ]
        )


class Comment(models.Model):
    """Комментарий под опубликованным постом."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Post')
    name = models.CharField(max_length=NAME_FIELD_MAX_LENGTH, verbose_name='Author')
    body = models.TextField(verbose_name='Content')
    email = models.EmailField(verbose_name='Email')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created datetime')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated datetime')
    active = models.BooleanField(default=True, verbose_name='Comment active status')

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"Комментарий к посту {self.post} от пользователя {self.name}"
