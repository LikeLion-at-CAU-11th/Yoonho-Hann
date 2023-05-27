from django.urls import path, include
from posts.views import *
from . import views
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#    # path('', hello_world, name = 'hello_world'),
#    # path('introduction', introduction, name = 'introduction'),
#    # path('<int:id>/', post_detail, name = 'post_detail'), # int 값을 받아서 pk인 id로 넘길 것
#    # path('', get_post_all, name = 'all_post'),
#    # path('time/', get_post_time, name = 'get_post_time'),
#    # path('new/', create_post, name="create_post"),
#    # path('comment/<int:id>/', get_comment, name='get_comment'),
#    # path('new_comment/', create_comment, name='create_comment')
#    
#    path('', PostList.as_view()),
#    path('<int:id>/', PostDetail.as_view()),
#    path('<int:id>/comments/', CommentList.as_view()),
#]

# urlpatterns = [
#    # path('', PostListMixins.as_view()),              - Mixin
#    # path('<int:pk>/', PostDetailMixins.as_view()),
#
#    # path('', PostListGenericAPIView.as_view()),      - GenericAPIView
#    # path('<int:pk>/', PostDetailGenericAPIView.as_view()),
#
#    # path('', post_list),                             - Viewset
#    # path('<int:pk>/', post_detail_vs),
# ]


router = DefaultRouter()                                # - Router
router.register('', views.PostViewSet)
router.register(r'(?P<post>\d+)/comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]