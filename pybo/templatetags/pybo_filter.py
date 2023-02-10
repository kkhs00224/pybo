"""
파일명 : pybo_filter.py
설 명 : 빼기 필터
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""
from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def mark(value):
    """입력된 문자열을 html로 변환"""
    # nl2br(줄바꿈 문자-> <br>, fenced_code(마크다운)
    extensions = ['nl2br', 'fenced_code']
    return mark_safe(markdown.markdown(value, extensions=extensions))

@register.filter
def sub(value, arg):
    """@register.filter: 템플릿에서 필터를 사용할 수 있게 된다.
        빼기 필터"""
    return value - arg
