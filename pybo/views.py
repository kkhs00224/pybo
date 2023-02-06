from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from pybo.models import Question
from django.utils import timezone
from pybo.models import Answer
from pybo.forms import QuestionForm, AnswerForm
import logging
from bs4 import BeautifulSoup
import requests


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
            question.save()  # 날짜까지 생성해서 저장(commit)
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


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
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        return HttpResponseNotAllowed('Post만 가능합니다.')
    # form validation
    context = {'question': question, 'form ': form}
    return render(request, 'pybo/question_detail.html', context)
    # return redirect('pybo:detail', question_id=question_id)

    # Question과 Answer처럼 서로 연결되어 있는 경우
    # 연결모델명_set 연결데이터를 조회할 수 있다.
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('pybo:detail', question_id=question_id)


def detail(request, question_id):
    """Question 상세"""
    logging.info('1.question_id:{}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    logging.info('2.question:{}'.format(question))
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def index(request):
    """Question 목록"""
    # list order create_date desc
    logging.info("index 레벨 출력")

    # 입력 인자: http://127.0.0.1:8000/pybo/2
    page = request.GET.get('page', '1')  # 페이지
    logging.info('page:{}'.format(page))

    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') DESC, order_by('필드') ASC
    # question_list = Question.objects.filter(id=99)  # order_by('-필드') DESC, order_by('필드') ASC

    # paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    # paginator.count : 전체 게시물 개수
    # paginator.per_page: 페이지당 보여줄 게시물 개수
    # paginator.page_range: 페이지 범위
    # number: 현재 페이지 번호
    # previous_page_number: 이전 페이지 번호
    # next_page_number: 다음 페이지 번호
    # has_previous: 이전 페이지 유무
    # has_next: 다음 페이지 유무
    # start_index: 현재 페이지 시작 인덱스(1부터 시작)
    # end_index: 현재 페이지 끝 인덱스

    context = {'question_list': page_obj}
    logging.info("page_obj:{}".format(page_obj))
    return render(request, 'pybo/question_list.html', context)
