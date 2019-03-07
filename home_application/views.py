# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/index.prod.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    """测试接口"""
    return render_json({'result': True, 'data': 'test api'})
