# -*- coding:utf-8 -*-

import django_filters
from django.contrib.auth.models import Group
from component.drf.filters import CaseInsensitiveBooleanFilter


class GroupFilter(django_filters.FilterSet):
    display_name = django_filters.CharFilter(name='groupprofile__display_name', lookup_expr='contains')
    is_enable = CaseInsensitiveBooleanFilter(name='groupprofile__is_enable', lookup_expr='eq')
    is_built_in = CaseInsensitiveBooleanFilter(name='groupprofile__is_enable', lookup_expr='eq')

    class Meta:
        model = Group
        fields = {
            'display_name': ['exact'],
            'is_enable': ['exact'],
            'is_built_in': ['exact'],
        }