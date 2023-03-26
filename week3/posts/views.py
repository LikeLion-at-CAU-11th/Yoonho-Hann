from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 

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
    