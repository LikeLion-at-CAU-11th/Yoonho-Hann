from django.urls import path
from posts.views import *

urlpatterns = [
    # path('', hello_world, name = 'hello_world'),
    # path('introduction', introduction, name = 'introduction'),
    path('<int:id>/', post_detail, name = 'post_detail'), # int 값을 받아서 pk인 id로 넘길 것
    path('', get_post_all, name = 'all_post'),
    path('time/', get_post_time, name = 'get_post_time'),
    path('new/', create_post, name="create_post"),
    path('comment/<int:id>/', get_comment, name='get_comment'),
    path('new_comment/', create_comment, name='create_comment')
]