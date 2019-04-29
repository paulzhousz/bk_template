# -*- coding: utf-8 -*-

from django.conf import settings


class CorsMiddleware(object):
    """xhr跨域中间件"""

    def process_response(self, request, response):
        if settings.RUN_MODE == 'DEVELOP':
            response['Access-Control-Allow-Origin'] = '*'
            if request.method == 'OPTIONS':
                response['Access-Control-Allow-Headers'] = 'content-type, accept, X-CSRFToken, X-Requested-With'
                response['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
                response.status_code = 200
        return response