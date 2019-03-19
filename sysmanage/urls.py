# -*- coding: utf-8 -*-

from rest_framework import routers as drf_routers
from sysmanage.views import (UserViewSet, GroupViewSet, PermViewSet, MenuViewSet)

routers = drf_routers.DefaultRouter(trailing_slash=True)

routers.register(r'user', UserViewSet, base_name='user')
routers.register(r'group', GroupViewSet, base_name='group')
routers.register(r'perm', PermViewSet, base_name='perm')
routers.register(r'menu', MenuViewSet, base_name='menu')

urlpatterns = routers.urls