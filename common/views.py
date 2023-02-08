from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm
import logging


# Create your views here.


def signup(request):
    """회원가입"""

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():  # post 방식에서 form이 유효한 경우
            # 회원가입
            form.save()
            # form username, password1
            username = form.cleaned_data.get('username')
            logging.info('username:{}'.format(username))

            password1 = form.cleaned_data.get('password1')
            logging.info('password1:{}'.format(password1))

            user = authenticate(username=username, password=password1)

            # 로그인
            login(request, user)

            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})