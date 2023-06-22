from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from .models import Post


def show_post_list(request: HttpRequest) -> HttpResponse:
    """Отобразить список постов и их содержимого."""
    posts = Post.published_posts.all()
    return render(
        request=request,
        template_name='blog/post/list.html',
        context={
            'posts': posts,
        }
    )


def show_post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Отобразить подробную информацию о посте."""
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={
            'post': post,
        }
    )

