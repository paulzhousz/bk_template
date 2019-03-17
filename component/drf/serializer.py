# -*- coding: utf-8 -*-

import warnings
from rest_framework import serializers
from django.conf import settings


class CustomSerializer(object):

    @staticmethod
    def to_internal_value(self, data):
        """实现部分更新功能（包括主外键、多对多）"""
        many_foreign_fields = {}
        foreign_field_names = getattr(self.Meta, 'foreign_fields', [])
        # 更新数据
        if self.instance:
            fields = self.fields.values()
            for field in fields:
                # 传入数据未包括必传参数，则用源数据替代
                if field.field_name not in data:
                    if getattr(field, 'many', False):
                        value = list(getattr(self.instance, field.field_name).values_list('pk', flat=True))
                        many_foreign_fields.update(**{field.field_name: value})
                    elif field.field_name in foreign_field_names:
                        value = getattr(self.instance, field.field_name)
                        many_foreign_fields.update(**{field.field_name + '_id': None if value is None else value.pk})
                    elif not getattr(field, 'read_only', False):
                        value = getattr(self.instance, field.field_name)
                        data.update(**{field.field_name: value})
                else:
                    if getattr(field, 'many', False):
                        many_foreign_fields.update(**{field.field_name: data[field.field_name]})
                    elif field.field_name in foreign_field_names:
                        many_foreign_fields.update(**{field.field_name + '_id': data[field.field_name]})
        # 创建数据
        else:
            fields = self.fields.values()
            for field in fields:
                if getattr(field, 'many', False):
                    many_foreign_fields.update(**{field.field_name: data[field.field_name]})
                elif field.field_name in foreign_field_names:
                    many_foreign_fields.update(**{field.field_name + '_id': data[field.field_name]})
        return data, many_foreign_fields


class DynamicFieldsMixin(object):
    """
    A serializer mixin that takes an additional `fields` argument that controls
    which fields should be displayed.
    """

    @property
    def fields(self):
        """
        Filters the fields according to the `fields` query parameter.
        A blank `fields` parameter (?fields) will remove all fields. Not
        passing `fields` will pass all fields individual fields are comma
        separated (?fields=id,name,url,email).
        """
        fields = super(DynamicFieldsMixin, self).fields

        if not hasattr(self, '_context'):
            # We are being called before a request cycle
            return fields

        # Only filter if this is the root serializer, or if the parent is the
        # root serializer with many=True
        is_root = self.root == self
        parent_is_list_root = self.parent == self.root and getattr(self.parent, 'many', False)
        if not (is_root or parent_is_list_root):
            return fields

        try:
            request = self.context['request']
        except KeyError:
            conf = getattr(settings, 'DRF_DYNAMIC_FIELDS', {})
            if not conf.get('SUPPRESS_CONTEXT_WARNING', False) is True:
                warnings.warn('Context does not have access to request. '
                              'See README for more information.')
            return fields

        # NOTE: drf test framework builds a request object where the query
        # parameters are found under the GET attribute.
        params = getattr(
            request, 'query_params', getattr(request, 'GET', None)
        )
        if params is None:
            warnings.warn('Request object does not contain query paramters')

        try:
            filter_fields = params.get('fields', None).split(',')
        except AttributeError:
            filter_fields = None

        try:
            omit_fields = params.get('omit', None).split(',')
        except AttributeError:
            omit_fields = []

        # Drop any fields that are not specified in the `fields` argument.
        existing = set(fields.keys())
        if filter_fields is None:
            # no fields param given, don't filter.
            allowed = existing
        else:
            allowed = set(filter(None, filter_fields))

        # omit fields in the `omit` argument.
        omitted = set(filter(None, omit_fields))

        for field in existing:

            if field not in allowed:
                fields.pop(field, None)

            if field in omitted:
                fields.pop(field, None)

        return fields


class ModelSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    pass
