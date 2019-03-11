#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from assets.models import IDC
from assets.models import BusinessUnit
from assets.utils.pager import PageInfo
from assets.utils.response import BaseResponse
from django.http.request import QueryDict
from assets.form import IdcForm


class IdcServer(object):
    @staticmethod
    def idc_condition(request):
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')

        return con_q

    @staticmethod
    def condition_config():
        values = [
            {'name': 'name', 'text': '机房', 'condition_type': 'input'},
            {'name': 'floor', 'text': '楼层', 'condition_type': 'input'},
        ]
        return values

    @staticmethod
    def table_config():
        values = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'name',
                'title': "机房",
                'display': 1,
                'attr': {'name': 'name', 'edit-enable': 'true', 'edit-type': 'input', }
            },
            {
                'q': 'floor',
                'title': "楼层",
                'display': 1,
                'attr': {'name': 'floor', 'edit-enable': 'true', 'edit-type': 'input', }
            },
        ]
        return values

    @classmethod
    def idc_values(cls):
        values = []
        for item in cls.table_config():
            values.append(item['q'])
        return values


    @staticmethod
    def idc_list():
        values = IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)



    @classmethod
    def fetch_assets(cls, request):
        response = BaseResponse()
        try:
            if request.GET.get('add', None):
                response.data = IdcForm().as_table()
                return response
            ret = {}
            conditions = cls.idc_condition(request)
            idc_count = IDC.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), idc_count)
            idc_list = IDC.objects.filter(conditions).values(*cls.idc_values())[
                         page_info.start:page_info.end]

            ret['table_config'] = cls.table_config()
            ret['condition_config'] = cls.condition_config()

            ret['data_list'] = list(idc_list)

            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }

            ret['global_dict'] = {
                'idc_list': cls.idc_list(),
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @classmethod
    def delete_assets(cls, request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            IDC.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @classmethod
    def put_assets(cls, request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    IDC.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num': num, 'message': str(e)})
                    response.status = False
                    error_count += 1
            if error_count:
                response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @classmethod
    def post_assets(cls, request):
        response = BaseResponse()
        add_dict = QueryDict(request.body, encoding='utf-8')
        data={}
        for k,v in add_dict.items():
            data[k]=v
        obj=IdcForm(data)
        if obj.is_valid():
            IDC.objects.create(**obj.cleaned_data)
            response.status=True
            return response
        else:
            response.status=False
            response.data=obj.as_table()
            return response



