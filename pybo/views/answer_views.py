"""
파일명 : answer_views.py
설 명 :
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from pybo.forms import AnswerForm
from pybo.models import Question, Answer


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    """답글 좋아요"""
    logging.info("1. answer_vote answer_id".format(answer_id))
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)

    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """답변 삭제"""
    logging.info('{}번 답변 삭제 시작'.format(answer_id))

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect(request, 'pybo:detail', question_id=answer.question.id)
    else:
        answer.delete()

    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """답변 수정"""
    logging.info('1. answer_modify:{}'.format(answer_id))
    # 1. answer_id 에 해당되는 데이터 조회
    # 2. 수정 권한 체크: 권한이 없는 경우 메시지 전달
    # 3. POST: 수정
    # 4. GET: 수정폼 전달

    # 1.
    answer = get_object_or_404(Answer, pk=answer_id)
    # 2.
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    # 3.
    if request.method == "POST":  # 수정
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            # answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

    else:  # 수정폼의 템플릿
        form = AnswerForm(instance=answer)

    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """답변 등록"""
    logging.info('answer_create question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)  # content만 저장(commit은 하지 않음)
            answer.question = question
            answer.create_date = timezone.now()
            answer.author = request.user  # author 속성에 로그인 계정 저장

            logging.info('3.answer.author:{}'.format(answer.author))
            answer.save()

            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question_id), answer.id))
    else:
        form = AnswerForm()

    # form validation
    context = {'question': question, 'form ': form}
    return render(request, 'pybo/question_detail.html', context)
    # return redirect('pybo:detail', question_id=question_id)

    # Question과 Answer처럼 서로 연결되어 있는 경우
    # 연결모델명_set 연결데이터를 조회할 수 있다.
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('pybo:detail', question_id=question_id)
