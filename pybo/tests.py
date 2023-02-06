import logging

from django.test import TestCase

# Create your tests here.
import unittest
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip  # 클립보드를 쉽게 활용할 수 있게 해주는 모듈
from selenium.webdriver.common.keys import Keys  # Ctrl + c, Ctrl + v

# from pybo.models import Question
# from django.utils import timezone
# q = Question(subject='금요일 입니다. [%3d]' % i, content='즐거운 금요일!', create_date=timezone.now())
# q.save()



class Crawling(unittest.TestCase):
    def setUp(self):
        # Webdriver
        self.browser = webdriver.Firefox(executable_path="C/BIG_AI010/01_PYTHO/ap/geckodriver.exe")
        print('setUp')

    def tearDown(self):
        print('tearDown')
        # self.browser.quit()  # webdriver 종료

    def test_clipboard_naver(self):
        """clipboard를 통한 naver login"""
        self.browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        user_id = 'kkhs224'
        user_pw = 'butterfly012!'

        # id
        id_textinput = self.browser.find_element(By.ID, 'id')
        id_textinput.click()
        # 클립보드로 copy
        pyperclip.copy(user_id)
        id_textinput.send_keys(Keys.CONTROL, 'v')  # 클립보드에서 id textinput으로 copy
        time.sleep(1)

        # password
        pw_textinput = self.browser.find_element(By.ID, 'pw')
        pw_textinput.click()
        pyperclip.copy(user_pw)
        pw_textinput.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 로그인 버튼
        btn_login = self.browser.find_element(By.ID, 'log.login')
        btn_login.click()

    @unittest.skip('테스트 연습6')
    def test_naver(self):
        self.browser.get("https://www.naver.com/")
        login = self.browser.find_element(By.CLASS_NAME, 'link_login')
        login.click()

        id = self.browser.find_element(By.ID, 'id')
        id.send_keys('kkhs224')
        pw = self.browser.find_element(By.ID, 'pw')
        pw.send_keys('1234')
        btn = self.browser.find_element(By.ID, 'log.login')
        btn.click()

    @unittest.skip('테스트 연습6')
    def test_selenium(self):
        # FireFox 웹 드라이버 객체에게 Get을 통하여 네이버의 http 요청을 하게 함.
        self.browser.get('http://127.0.0.1:8000/pybo/5/')
        print('self.browser.title:{}'.format(self.browser.title))
        self.assertIn('Pybo', self.browser.title)

        content_textarea = self.browser.find_element(By.ID, 'content')
        content_textarea.send_keys('오늘은 아주 슬픈 금요일!33')
        btn = self.browser.find_element(By.ID, 'submit_btn')
        btn.click()
        # form = self.browser.find_element(By.NAME, 'answer_frm')
        # form.submit()

    @unittest.skip('테스트 연습5')
    def test_zip(self):
        """여러 개의 list를 묶어서 하나의 iterable 객체로 다룰 수 있게 한다."""
        intergers = [1, 2, 3]
        letters = ['a', 'b', 'c']
        floats = [4.0, 8.0, 10.0]
        zipped = zip(intergers, letters, floats)
        list_data = list(zipped)
        print('list_data:{}'.format(list_data))

    @unittest.skip('테스트 연습4')
    def test_naver_stock(self):
        codes = {'삼성전자': '005930', '현대차': '005380'}
        for code in codes.keys():
            url = "https://finance.naver.com/item/main.naver?code="
            url = url + str(codes[code])

            resp = requests.get(url)
            if resp.status_code == 200:
                html = resp.text
                soup = BeautifulSoup(html, 'html.parser')
                # 제목
                price = soup.select_one('#chart_area div.rate_info div.today span.blind')
                print('today:{}, {}, {}'.format(code, codes[code], price.getText()))
            else:
                print('접속 오류:{}'.format(resp.status_code))

    @unittest.skip('테스트 연습3')
    def test_slamdunk(self):
        """https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&target=after&page=1"""
        url = "https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&target=after"
        for page in range(3):
            url_page = url + "&page={}".format(page + 1)
            print(url_page)
            resp = requests.get(url_page)
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            # 영화 제목
            movie_title = soup.select("tbody tr td.title a.movie")
            # 평점
            score = soup.select("div.list_netizen_score em")
            report_list = soup.select("td.title a.report")
            for row in range(len(report_list)):
                report_o = report_list[row].get('onclick')
                report = report_o[7:-2].split(',')
                # 작성자
                user = report[0].strip().strip("'")
                # 감상평
                review = report[2].strip().strip("'")
                # 등록 번호
                reg_num = report[3].strip().strip("'")
                print("등록번호:{}, 영화 제목:{}, 평점:{}, 감상평:{}, 작성자:{}".format(reg_num, movie_title[row].getText(),
                                                                        score[row].getText(), review, user))

    @unittest.skip('테스트 연습2')
    def test_cgv(self):
        """CGV http://www.cgv.co.kr/movies/?lt=1&ft=0"""
        url = "http://www.cgv.co.kr/movies/?lt=1&ft=0"
        resp = requests.get(url)
        if resp.status_code == 200:
            html = resp.text
            # print("html:{}".format(html))
            # box-contents
            soup = BeautifulSoup(html, 'html.parser')
            # 제목
            title = soup.select("div.box-contents strong.title")
            # 예매율
            reserve = soup.select("div.box-contents div.score strong.percent")
            # 영화 포스터 사진
            poster = soup.select("div.box-image span.thumb-image img")

            for page in range(7):
                poster_img = poster[page]
                # img_url_path = poster_img.get_attribute_list('src')
                img_url_path = poster_img.get('src')  # <img src='' />에 접근
                # print(img_url_path)
                print(
                    "영화 제목:{}, 예매율:{}, 이미지 경로:{}".format(title[page].getText(), reserve[page].getText(), img_url_path))

        else:
            print("접속 오류 response.status_code:{}".format(resp.status_code))

    @unittest.skip('테스트 연습')
    def test_weather(self):
        """날씨  """
        # https://weather.naver.com/today/09545101
        now = datetime.datetime.now()
        # yyyymmdd hh:mm
        now.strftime("%Y-%m-%d, %H:%M:%S")
        print('=' * 35)
        print("now:{}".format(now))
        print('=' * 35)
        # -----------------------------------------------------
        naver_weather_url = "https://weather.naver.com/today/09545101"
        html = urlopen(naver_weather_url)
        # print("html:{}".format(html))
        bs_object = BeautifulSoup(html, 'html.parser')
        tempes = bs_object.find("strong", "current")
        print("날씨:{}".format(tempes.getText()))

        print('test_weather')
