# -*- coding: utf-8 -*-

from rest_framework import routers as drf_routers
from sysmanage.views import (UserViewSet, GroupViewSet, PermViewSet, MenuViewSet, MockViewSet, LogViewSet)

routers = drf_routers.DefaultRouter(trailing_slash=True)

routers.register(r'users', UserViewSet, base_name='user')
routers.register(r'groups', GroupViewSet, base_name='group')
routers.register(r'perms', PermViewSet, base_name='perm')
routers.register(r'menus', MenuViewSet, base_name='menu')
routers.register(r'mocks', MockViewSet, base_name='mock')
routers.register(r'logs', LogViewSet, base_name='log')

urlpatterns = routers.urls