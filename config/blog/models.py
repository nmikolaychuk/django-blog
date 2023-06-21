from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


TEXT_FIELD_MAX_LENGTH = 250
STATUS_FIELD_MAX_LENGTH = 2


class Post(models.Model):
    """Пост блога."""

    class Status(models.TextChoices):
        """Статус поста."""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH)
    slug = models.SlugField(max_length=TEXT_FIELD_MAX_LENGTH)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=STATUS_FIELD_MAX_LENGTH, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]

    def __str__(self):
        return self.title
