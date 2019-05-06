# -*- coding:utf-8 -*-

"""
drf filters
"""

import django_filters
from django.contrib.auth import get_user_model
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


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name='username', lookup_expr='icontains')
    chname = django_filters.CharFilter(name='chname', lookup_expr='contains')
    email = django_filters.CharFilter(name='email', lookup_expr='icontains')
    is_enable = CaseInsensitiveBooleanFilter(name='is_enable', lookup_expr='eq')
    is_in_app = CaseInsensitiveBooleanFilter(name='is_in_app', lookup_expr='eq')

    class Meta:
        model = get_user_model()
        fields = {
            'username': ['exact'],
            'chname': ['exact'],
            'email': ['exact'],
            'is_enable': ['exact'],
            'is_in_app': ['exact'],
        }