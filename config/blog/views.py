from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings

from .models import Post
from .forms import EmailPostForm


POSTS_ON_LIST = 2
FIRST_PAGE_NUMBER = 1


def share_post_by_email(request: HttpRequest, post_id: int) -> HttpResponse:
    """Поделиться постом по email."""
    post = get_object_or_404(klass=Post, pk=post_id, status=Post.Status.PUBLISHED)
    is_sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if not form.is_valid():
            pass
        # Получение и отрпавка по email данных из формы.
        cleaned_data = form.cleaned_data
        post_url = request.build_absolute_uri(location=post.get_absolute_url())
        subject = f"Пользователь {cleaned_data['name']} рекомендует Вам прочесть пост \"{post.title}\""
        message = f"Вам может быть интересен пост \"{post.title}\": {post_url}\n\n" \
                  f"Комментарий пользователя {cleaned_data['name']}: {cleaned_data['comments']}"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[cleaned_data['to']]
        )
        is_sent = True
    else:
        form = EmailPostForm()
    return render(
        request=request,
        template_name='blog/post/share.html',
        context={
            'post': post,
            'form': form,
            'sent': is_sent,
        }
    )


def show_post_list(request: HttpRequest) -> HttpResponse:
    """Отобразить список постов и их содержимого."""
    post_list = Post.published_posts.all()
    paginator = Paginator(object_list=post_list, per_page=POSTS_ON_LIST)
    page_number = request.GET.get('page', FIRST_PAGE_NUMBER)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(FIRST_PAGE_NUMBER)
    return render(
        request=request,
        template_name='blog/post/list.html',
        context={
            'posts': posts,
        }
    )


def show_post_detail(request: HttpRequest, year: int, month: int, day: int, post: str) -> HttpResponse:
    """Отобразить подробную информацию о посте."""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        published__year=year,
        published__month=month,
        published__day=day,
    )
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={
            'post': post,
        }
    )

