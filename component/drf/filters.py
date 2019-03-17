# -*- coding: utf-8 -*-

import django_filters


class CaseInsensitiveBooleanFilter(django_filters.Filter):
    """布尔类型值筛选"""

    def filter(self, qs, value):
        if value is not None:
            lc_value = value.lower()
            if lc_value == "true":
                value = True
            elif lc_value == "false":
                value = False
            return qs.filter(**{self.name: value})
        return qs
