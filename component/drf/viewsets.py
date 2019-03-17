# -*- coding: utf-8 -*-

from rest_framework import viewsets
from component.drf.mixins import ApiGenericMixin


class ModelViewSet(ApiGenericMixin, viewsets.ModelViewSet):
    pass


class ViewSet(ApiGenericMixin, viewsets.ViewSet):
    pass


class GenericViewSet(ApiGenericMixin, viewsets.GenericViewSet):
    pass
