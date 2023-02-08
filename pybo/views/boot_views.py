"""
파일명 : boot_views.py
설 명 :
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer

# bootstrap list
def boot_menu(request):
    """개발에 사용되는 임시 메뉴"""
    return render(request, "pybo/menu.html")


def boot_reg(request):
    """bootstrap reg template"""
    return render(request, "pybo/reg.html")


def boot_list(request):
    """bootstrap template"""
    return render(request, "pybo/list.html")


def crawling_cgv(request):
    """cgv 영화 차트"""
    url = "http://www.cgv.co.kr/movies/?lt=1&ft=0"
    resp = requests.get(url)
    context = {}
    if resp.status_code == 200:
        html = resp.text
        # print("html:{}".format(html))
        # box-contents
        soup = BeautifulSoup(html, 'html.parser')
        # 제목
        title = soup.select("div.box-contents strong.title")
        # 예매율
        reserve = soup.select("div.box-contents div.score strong.percent")

        # context = {'title':title}
        # 영화 포스터 사진
        poster = soup.select("div.box-image span.thumb-image img")

        title_list = []
        reserve_list = []
        poster_list = []
        for page in range(7):
            poster_img = poster[page]
            # img_url_path = poster_img.get_attribute_list('src')
            img_url_path = poster_img.get('src')  # <img src='' />에 접근
            # print(img_url_path)
            title_list.append(title[page].getText())
            reserve_list.append(reserve[page].getText())
            poster_list.append(img_url_path)
            print(
                "영화 제목:{}, 예매율:{}, 이미지 경로:{}".format(title[page].getText(), reserve[page].getText(), img_url_path))
        context = {'context': zip(title_list, reserve_list, poster_list)}
    else:
        print("접속 오류 response.status_code:{}".format(resp.status_code))
    return render(request, 'pybo/crawling_cgv.html', context)

