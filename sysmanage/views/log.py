# -*- coding: utf-8 -*-

from component.drf.viewsets import ModelViewSet
from sysmanage.models import Log
from sysmanage.serializers import LogSerializer
from sysmanage.filters import LogFilter


class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_class = LogFilter
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """获取操作日志分页数据"""
        return super(LogViewSet, self).list(request, *args, **kwargs)
