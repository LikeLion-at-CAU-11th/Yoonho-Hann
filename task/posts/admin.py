from django.contrib import admin
from .models import Post, Comment   # . -> 현재 디렉토리


# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)