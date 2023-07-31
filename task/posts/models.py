from django.db import models
from accounts.models import Member


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):

    CHOICES = (     # 부가적
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    post_id = models.AutoField(primary_key=True)            # 자동 - 따로 입력받지 않음
    # writer = models.CharField(verbose_name="작성자", max_length=30)     # max_length 필수
    writer = models.ForeignKey(to=Member, on_delete=models.CASCADE, verbose_name="작성자")
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)
    thumbnail = models.ImageField(null=True, verbose_name="이미지")

class Comment(BaseModel):
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False)
    # CASECADE -> 게시글 삭제시 댓글도 삭제