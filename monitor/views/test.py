# -*- coding: utf-8 -*-

import random
from faker import Faker
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from component.drf.viewsets import ViewSet


class MockViewSet(ViewSet):
    http_method_names = ['get']

    @list_route(methods=['get'], url_path='task/state')
    def get_task_state(self, request, *args, **kwargs):
        """
        获取任务状态数据

            返回结果
            {
              "result": true,
              "message": "success",
              "code": "OK",
              "data": {
                "fail": 23,
                "running": 39,
                "waitting": 34,
                "success": 32
              }
            }
            - waitting 等待中
            - running 运行中
            - success 已成功
            - fail 已失败

        """
        ret = {'waitting': random.randint(1, 50), 'running': random.randint(1, 50), 'success': random.randint(1, 50),
               'fail': random.randint(1, 50)}
        return Response(ret)

    @list_route(methods=['get'], url_path='server/select')
    def get_server_select(self, request, *args, **kwargs):
        """
        获取服务器下拉框数据

            返回结果：
            {
              "result": true,
              "message": "success",
              "code": "OK",
              "data": [
                {
                  "ip": "192.168.10.10",
                  "id": 1
                },
                {
                  "ip": "192.168.10.11",
                  "id": 2
                }
              ]
            }
        """
        ret = [
            {'id': 1, 'ip': '192.168.10.10'},
            {'id': 2, 'ip': '192.168.10.11'},
            {'id': 3, 'ip': '192.168.10.12'},
            {'id': 4, 'ip': '192.168.10.13'},
            {'id': 5, 'ip': '192.168.10.14'},
        ]
        return Response(ret)

    @detail_route(methods=['get'], url_path='server/performance')
    def get_server_performance(self, request, *args, **kwargs):
        """
        获取服务器性能数据

            返回结果:
            {
              "result": true,
              "message": "success",
              "code": "OK",
              "data": [
                {
                  "product": "0:00",
                  "mem": 89,
                  "cpu": 74
                },
                {
                  "product": "1:00",
                  "mem": 90,
                  "cpu": 80
                }
              ]
            }
            - product x轴数据 时间点
            - mem 内存百分比
            - cpu CPU百分比
        """
        xtime = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
                 '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00',
                 '23:00']
        ret = [{'product': x, 'cpu': random.randint(50, 100), 'mem': random.randint(50, 100)} for x in xtime]
        return Response(ret)

    @list_route(methods=['get'], url_path='biz/server')
    def get_biz_server(self, request):
        """
        获取业务下服务器数量

            返回结果:
            {
              "result": true,
              "message": "success",
              "code": "OK",
              "data": [
                {
                  "product": "IT",
                  "windows": 50,
                  "linux": 60
                },
                {
                  "product": "销售",
                  "windows": 40,
                  "linux": 30
                }
              ]
            }
            - product x轴数据 部门
            - windows Windows服务器数量
            - linux Linux服务器数量
        """
        ret = [
            {'product': 'IT', 'windows': 50, 'linux': 60},
            {'product': '销售', 'windows': 40, 'linux': 30},
            {'product': '财务', 'windows': 10, 'linux': 15},
            {'product': 'HR', 'windows': 5, 'linux': 15},
        ]
        return Response(ret)