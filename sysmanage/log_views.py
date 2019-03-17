# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from sysmanage.models import Log, LogObject, LogType
from .serializers import LogSerializer
from common.mymako import render_json
import xlwt
from django.http import HttpResponse, JsonResponse
import datetime
from common.log import logger
from .utils import log_to_db
from sysmanage.decorators import perm_required


# Create your views here.

def search_log(request):
    """获取日志列表"""
    try:
        params_dict = request.GET
        condition_filter = {}
        operator = params_dict.get('operator', '')
        operated_type = params_dict.get('operated_type', '')
        operated_object = params_dict.get('operated_object', '')
        start_time = params_dict.get('start_time', '')
        end_time = params_dict.get('end_time', '')
        is_success = params_dict.get('is_success', '')
        if is_success:
            condition_filter['is_success'] = is_success
        if operator:
            condition_filter['operator__icontains'] = operator
        if operated_type:
            condition_filter['operated_type__icontains'] = operated_type
        if operated_object:
            condition_filter['operated_object__icontains'] = operated_object
        if start_time:
            t_to_str = start_time.replace('&nbsp;', ' ')
            start_time = datetime.datetime.strptime(t_to_str, '%Y-%m-%d %H:%M:%S')
            condition_filter['operator_date__gte'] = start_time
        if end_time:
            t_to_str = end_time.replace('&nbsp;', ' ')
            end_time = datetime.datetime.strptime(t_to_str, '%Y-%m-%d %H:%M:%S')
            condition_filter['operator_date__lte'] = end_time
        logs = Log.objects.filter(**condition_filter)
        # 每页多少条数据
        per_page = params_dict.get('number_pieces', 10)
        paginator = Paginator(logs, per_page)
        try:
            log_page = paginator.page(params_dict.get('requested_page', 1))
        except PageNotAnInteger:
            log_page = paginator.page(1)
        except EmptyPage:
            # 指定页码超出范围
            log_page = paginator.page(paginator.num_pages)
        log_serializer = LogSerializer(log_page, many=True)
        return render_json(
            {'result': True, 'code': 0, 'message': u'获取日志列表成功',
             'data': {'log': log_serializer.data, 'count': paginator.count}}
        )
    except Exception as e:
        return render_json(
            {
                "result": False, "code": 1, 'message': u'获取日志列表失败',

            }
        )


@perm_required('sysmanage.export_log')
def export_log_to_excel(request):
    """日志导出"""
    try:
        style_bold_red = xlwt.easyxf('font:color-index blue,bold on')
        header_style = style_bold_red  # 设置表头样式
        wb = xlwt.Workbook()  # 创建一个book
        ws = wb.add_sheet('sheet1')  # 添加一个工作表
        ws.write(0, 0, u"操作时间", header_style)
        ws.write(0, 1, u"操作账号", header_style)
        ws.write(0, 2, u"操作对象", header_style)
        ws.write(0, 3, u"操作类型", header_style)
        ws.write(0, 4, u"IP地址", header_style)
        ws.write(0, 5, u"操作内容", header_style)
        ws.write(0, 6, u"操作结果", header_style)
    except Exception as e:
        logger.exception(e)
        result = {
            'result': False,
            "message": u"创建excel文件失败"
        }
        return JsonResponse(result)
    try:
        log_id = request.GET.get('log_id_str', "").encode('utf-8')
        if log_id:
            try:
                log_id_list = log_id.split(",")
                gathers = Log.objects.filter(id__in=log_id_list).order_by('-id')
            except Exception as e:
                logger.exception(e)
                result = {
                    "result": False,
                    "message": u"查询数据库错误"
                }
                return JsonResponse(result)
        else:
            gathers = Log.objects.all().order_by('-id')
        j = 1
        for gather in gathers:
            value = []
            value.append(gather.operator_date)
            value.append(gather.operator)
            value.append(gather.operated_object)
            value.append(gather.operated_type)
            value.append(gather.ip_addr)
            value.append(gather.content)
            if gather.is_success:
                value.append(u'操作成功')
            else:
                value.append(u'操作失败')
            # 按索引得到对应的sheet
            log_info = wb.get_sheet(0)
            for i in range(0, 7):
                if isinstance(value[i], unicode):
                    v = value[i]
                else:
                    v = str(value[i])
                log_info.write(j, i, v)
            j += 1
        response = HttpResponse(content_type='application/vnd.ms-excel', charset='utf-8')
        response['Content-Disposition'] = r'attachment; filename=LOG' \
                                          + datetime.datetime.now().strftime('%Y%m%d') + '.xls'
        wb.save(response)
        # log
        operated_object = u'操作日志'
        operated_type = u'导出'
        content = u'操作日志导出成功'
        log_to_db(request, operated_object, operated_type, content)
        return response
    except Exception as e:
        result = {'result': False, "error": e, "message": "导出失败"}
        logger.exception(e)
        # log
        operated_object = u'操作日志'
        operated_type = u'导出'
        content = u'操作日志导出失败'
        is_success = False
        log_to_db(request, operated_object, operated_type, content, is_success)
        return JsonResponse(result)


def get_select_log_object(request):
    """
    获取查询的操作对象
    :param request:
    :return:
    """
    try:
        log_objects = LogObject.objects.values('operated_object')
        data = []
        for i in log_objects:
            data.append(i['operated_object'])
        result = {
            "result": True,
            "message": u"查询成功",
            "data": data
        }
        return JsonResponse(result)
    except Exception as e:
        logger.exception(e)
        result = {
            "result": False,
            "message": u"查询失败",
            "error": "{}".format(e)
        }
        return JsonResponse(result)


def get_select_log_type(request):
    """
    获取查询的操作类型
    :param request:
    :return:
    """
    try:
        log_types = LogType.objects.values('operated_type')
        data = []
        for i in log_types:
            data.append(i['operated_type'])
        result = {
            "result": True,
            "message": u"查询成功",
            "data": data
        }
        return JsonResponse(result)
    except Exception as e:
        logger.exception(e)
        result = {
            "result": False,
            "message": u"查询失败"
        }
        return JsonResponse(result)
