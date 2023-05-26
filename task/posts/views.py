from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
from django.views.decorators.http import require_http_methods

from .models import Post, Comment
import json

from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# from django.http import HttpResponse

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data': "Hello world",
        })
    
def introduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data': [{
                "name" : "한윤호",
                "age" : 23,
                "major" : "Computer Science and Engineering"
            }, {
                "name" : "배영경",
                "age" : 21,
                "major" : "Computer Science and Engineering"
            }],
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk = id)
        category_json = {
            "id" : post.post_id,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        }

        return JsonResponse({
            'status' : 200,
            'message' : '게시글 조회 성공',
            'data' : category_json
        })
    
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk = id)

        update_post.content = body['content']
        update_post.category = body['category']
        update_post.save()      # 변동사항 DB에 저장 - ORM 제공됨

        update_post_json = {
            "id": update_post.post_id,
            "writer": update_post.writer,
            "content": update_post.content,
            "category": update_post.category
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    elif request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk = id)
        delete_post.delete()

        return JsonResponse({
            'status': 200,
            'message': '게시글 삭제 성공',
            'data': None
        })

@require_http_methods(["GET"])
def get_post_all(request):
    post_json_all = []
    post_list = Post.objects.all()

    for post in post_list:
        post_json_all.append({
            "id" : post.post_id,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        })

    return JsonResponse({
        'status' : 200,
        'message' : '전체 게시글 조회 성공',
        'data' : post_json_all
    })

@require_http_methods(["GET"])                              # 4주차 챌린지 미션                                         # RuntimeWarning 발생 -> USE_TZ = False로 해결 ?
def get_post_time(request):
    post_json_all = []
    post_list = Post.objects.filter(created_at__range=('2023-04-05 22:00:00', '2023-04-12 19:00:00'))

    for post in post_list:
        post_json_all.append({
            "id" : post.post_id,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        })

    return JsonResponse({
        'status' : 200,
        'message' : '챌린지 미션 조회 성공',
        'data' : post_json_all
    })


@require_http_methods(["POST"])
def create_post(request):
    body = json.loads(request.body.decode('utf-8'))

    new_post = Post.objects.create(
        writer = body['writer'],
        content = body['content'],
        category = body['category']
    )

    new_post_json = {
        "id": new_post.post_id,
        "writer": new_post.writer,
        "content": new_post.content,
        "category": new_post.category
    }

    return JsonResponse({
        'status': 200,
        'message': '게시글 생성 성공',
        'data': new_post_json
    })

@require_http_methods(["GET"])
def get_comment(request, id):
    comment_all = Comment.objects.filter(post = id)
    comment_json_list = []

    for comment in comment_all:
        comment_json_list.append({
            'writer': comment.writer,
            'content': comment.content
        })
    
    return JsonResponse({
        'status': 200,
        'message': "댓글 조회 성공",
        'data': comment_json_list
    })

@require_http_methods(["POST"])
def create_comment(request):                                # 4주차 스탠다드 - 댓글 작성 API
    body = json.loads(request.body.decode('utf-8'))

    comment_post = Post.objects.get(post_id = body["id"])

    new_comment = Comment.objects.create(
        writer = body['writer'],
        content = body['content'],
        post = comment_post
    )

    new_post_json = {
        "writer": new_comment.writer,
        "content": new_comment.content,
        "post": body['id']
    }

    return JsonResponse({
        'status': 200,
        'message': '댓글 생성 성공',
        'data': new_post_json
    })


##################### DRF #####################

class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)   # 받아올 데이터가 복수개면 (many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, id):
        post = get_object_or_404(Post, pk=id)           
        serializer = PostSerializer(post, data=request.data)        # 수정할 post 지정하고 업데이트 -> post와 동일
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentList(APIView):                              # 8주차 챌린지 미션
    def post(self, request, id, format=None):
        comment_post = Post.objects.get(post_id=id)
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(post=comment_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        comment_all = Comment.objects.filter(post = id)
        serializer = CommentSerializer(comment_all, many=True)
        return Response(serializer.data)
    

from rest_framework import mixins, generics

class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

# Mixins - 클래스 상속을 통해 새로운 속성이나 기능을 추가
class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  # 단일 객체 리턴
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# GenericAPIView - 한 번에 상속 받기
class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Viewset - 헬퍼클래스
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# post_list = PostViewSet.as_view({
#    'get': 'list',
#    'post': 'create'
# })

# post_detail_vs = PostViewSet.as_view({
#    'get': 'retrieve',
#    'put': 'update',
#    'patch': 'partial_update',
#    'delete': 'destroy'
# })