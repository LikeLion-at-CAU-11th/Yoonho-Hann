from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):     # AbstractUser 상속
    age = models.IntegerField(verbose_name="나이",default=20, null=True)
    # verbose_name (부가 속성 - admin 페이지에서 보이는 설명) 필수 아님