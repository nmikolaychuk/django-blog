from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


TEXT_FIELD_MAX_LENGTH = 250
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

    title = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH)
    slug = models.SlugField(max_length=TEXT_FIELD_MAX_LENGTH, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=STATUS_FIELD_MAX_LENGTH, choices=Status.choices, default=Status.DRAFT)
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
