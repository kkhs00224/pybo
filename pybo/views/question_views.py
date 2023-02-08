"""
파일명 : question_views.py
설 명 :
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def question_create(request):
    """질문 등록"""
    logging.info("1. request.method:{}".format(request.method))
    if request.method == 'POST':
        logging.info('2. question_create post')
        # 저장
        form = QuestionForm(request.POST)  # request.POST

        if form.is_valid():  # form(질문 등록)이 유효하면
            question = form.save(commit=False)  # subject, content만 저장(commit은 하지 않음)
            question.create_date = timezone.now()
            question.author = request.user  # author 속성에 로그인 계정 저장

            logging.info('4.question.author:{}'.format(question.author))

            question.save()  # 날짜까지 생성해서 저장(commit)
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url="common:login")
def question_modify(request, question_id):
    """질문 수정 : login 필수"""
    logging.info("1. question_modify")
    question = get_object_or_404(Question, pk=question_id)  # question_id 로 Question 조회

    # 권한 체크
    if request.user != question.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect("pybo:detail", question_id=question.id)

    if request.method == 'POST':
        logging.info('2.question_modify post')
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            logging.info('3.form.is_valid():{}'.format(form.is_valid()))
            question = form.save(commit=False)  # 질문 내용,
            question.modify_date = timezone.now()  # 수정 일시 저장
            question.save()  # 수정 일시까지 저장
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


def question_delete(request, question_id):
    logging.info('1. question_delete')
    logging.info('2. question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error('삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    question.delete()
    return redirect('pybo:index')
