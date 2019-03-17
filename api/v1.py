# -*- coding:utf-8 -*-

from django.conf.urls import include, patterns, url

# 公共URL配置
urlpatterns = patterns(
    '',
    # 权限管理
    url(r'^sysmanage/', include('sysmanage.urls')),
    url(r'^', include('home_application.urls'))
)