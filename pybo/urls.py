"""
파일명 : urls.py
설 명 : pybo 모든 URL과 VIEW 함수의 매핑 담당
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""

from django.urls import path
from . import views  # 현재 디렉토리의 views 모듈

app_name = 'pybo'

urlpatterns = [
    path("", views.index, name='index'),  # views index로 매핑
    path("<int:question_id>/", views.detail, name='detail'),
    path("answer/create/<int:question_id>/", views.answer_create, name='answer_create'),
    path("question/create/", views.question_create, name='question_create'),

    # temp menu
    path("boot/menu/", views.boot_menu, name="boot_menu"),
    # bootstrap template
    path("boot/list/", views.boot_list, name="boot_list"),
    path("boot/reg/",views.boot_reg, name="boot_reg"),

    path('crawling/cgv/',views.crawling_cgv, name='crawling_cgv')
]
