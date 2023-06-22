from django.urls import path
from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.show_post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.show_post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.share_post_by_email, name='share_post_by_email'),
]
