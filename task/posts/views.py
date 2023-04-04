from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
from django.views.decorators.http import require_http_methods
from .models import Post

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
    
@require_http_methods(["GET"])
def get_post_detail(request, id):
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

@require_http_methods(["GET"])
def get_all_post(request):
    results = []
    post_list = Post.objects.all()

    for i in post_list:
        results.append({
            "id" : i.post_id,
            "writer" : i.writer,
            "content" : i.content,
            "category" : i.category,
        })

    return JsonResponse({
        'status' : 200,
        'message' : '전체 게시글 조회 성공',
        'data' : results
    })