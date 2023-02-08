"""
파일명 : forms.py
설 명 : 회원가입 폼
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        # password1, password2 (비밀번호1을 제대로 입력했는지 대조하기 위한 값)
        fields = ('username', 'password1', 'password2', 'email')
