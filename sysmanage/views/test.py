# -*- coding: utf-8 -*-

# from faker import Faker
from django.contrib.auth import get_user_model
from rest_framework.decorators import list_route
from rest_framework.response import Response
from component.drf.viewsets import ViewSet


class MockViewSet(ViewSet):
    http_method_names = ['get']

    @list_route(methods=['get'], url_path='init/user')
    def init_user(self, request, *args, **kwargs):
        """
        新增用户模拟数据

            /api/sysmanage/mocks/init/user/?count=30
            -count 插入用户数量(默认30) Number【选填】
        """
        count = request.data.get('count', 30)
        faker = Faker(locale='zh_CN')
        bulk_list = []
        for i in range(count):
            bulk_list.append(
                get_user_model()(username=faker.user_name(), chname=faker.name(), is_in_app=True, is_enable=True)
            )
        get_user_model().objects.bulk_create(bulk_list)
        return Response()