from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('introduction', introduction, name = 'introduction'),
    path('post_detail/<int:id>/', get_post_detail, name = 'post_detail'), # int 값을 받아서 pk인 id로 넘길 것
    path('post_detail/', get_all_post, name = 'all_post'),
]