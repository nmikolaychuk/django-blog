from django.urls import path
from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.show_post_list, name='post_list'),
    path('<int:post_id>/', views.show_post_detail, name='post_detail'),
]
