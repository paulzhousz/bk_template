# -*- coding: utf-8 -*-

from rest_framework import routers as drf_routers
from monitor.views.test import MockViewSet

routers = drf_routers.DefaultRouter(trailing_slash=True)

routers.register('mocks', MockViewSet, base_name='mock')

urlpatterns = routers.urls
