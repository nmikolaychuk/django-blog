from django import template
from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    """Тег для получения общего количества опубликованных постов."""
    return Post.published_posts.count()
