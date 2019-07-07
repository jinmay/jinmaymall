from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=100,
        unique=True,
        validators=[username_validator],
        error_messages = {
            'unique': '이미 존재하는 username입니다.'
        }
    )
    email = models.EmailField()
    is_staff = models.BooleanField(default=False, help_text="어드민 패널을 사용할 수 있는 관리자입니다.")
    is_active = models.BooleanField(default=True, help_text="활성화된 계정")
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']