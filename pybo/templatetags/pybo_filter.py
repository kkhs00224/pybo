"""
파일명 : pybo_filter.py
설 명 : 빼기 필터
생성일 : 
생성자 : Kim
since 2023.01.10 Copyright (C) by '' All right reserved. 
"""
from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    """@register.filter: 템플릿에서 필터를 사용할 수 있게 된다.
        빼기 필터"""
    return value - arg
