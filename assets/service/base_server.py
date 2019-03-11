#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from assets.utils.pager import PageInfo
from assets.utils.response import BaseResponse
from django.http.request import QueryDict
from assets.models import Asset,IDC,BusinessUnit,Server,RemoteUser
# from assets.models import BusinessUnit
from assets.service.condition_config import ConditionConfig


class BaseServers(object):
    # __response=BaseResponse()
    def __init__(self, request,server,data,form=None,add=True,put_data=None,post_data=None):
        self.request = request
        self.server=server
        self.data = data
        self.form=form
        self.add=add
        self.put_data=put_data
        self.post_data=post_data
        self.response = BaseResponse()

    @property
    def search_condition(self):
        con_str = self.request.GET.get('condition', None)
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

    def get_server(self):
        try:
            if self.add:
                if self.request.GET.get('add', None):
                    self.response.data = self.form().as_table()
                    return self.response
            ret = {}
            conditions = self.search_condition
            counts = self.data.objects.filter(conditions).count()
            page_info = PageInfo(self.request.GET.get('pager', None), counts)
            value_list = self.data.objects.filter(conditions).values(*ConditionConfig.choice_values(self.server))[
                       page_info.start:page_info.end]

            ret['table_config'] = ConditionConfig.choice_table_config(self.server)
            ret['condition_config'] = ConditionConfig.choice_config(self.server)

            ret['data_list'] = list(value_list)

            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }

            ret['global_dict']=self.choice_global_dict()
            self.response.data = ret
            self.response.message = '获取成功'

        except Exception as e:
            self.response.status = False
            self.response.message = str(e)
        return self.response

    # def get_server_host(self):
    #     try:
    #         if self.add:
    #             if self.request.GET.get('add', None):
    #                 self.response.data = self.form().as_table()
    #                 return self.response
    #         ret = {}
    #         conditions = self.search_condition
    #         counts = self.data.objects.filter(conditions).count()
    #         page_info = PageInfo(self.request.GET.get('pager', None), counts)
    #         value_list = self.data.objects.filter(conditions).values(*ConditionConfig.choice_values(self.server))[
    #                    page_info.start:page_info.end]
    #         ret['table_config'] = ConditionConfig.choice_table_config(self.server)
    #         ret['condition_config'] = ConditionConfig.choice_config(self.server)
    #
    #         ret['data_list'] = list(value_list)
    #
    #         ret['page_info'] = {
    #             "page_str": page_info.pager(),
    #             "page_start": page_info.start,
    #         }
    #
    #         ret['global_dict']=self.choice_global_dict()
    #         self.response.data = ret
    #         self.response.message = '获取成功'
    #
    #     except Exception as e:
    #         self.response.status = False
    #         self.response.message = str(e)
    #     return self.response

    def choice_global_dict(self):
        values = '%s_%s' % ('global_dict',self.server)
        if hasattr(self, values):
            func = getattr(self, values)
            return func()
        else:
            return

    def global_dict_idc(self):
        result = {
            'idc_list': self.idc_list(),
        }
        return result

    def global_dict_asset(self):
        result = {
             'device_status_list': self.device_status_list(),
             'device_type_list': self.device_type_list(),
             'idc_list': self.idc_list(),
             'business_unit_list': self.business_unit_list(),
        }
        return result

    def global_dict_bindhost(self):
        result = {
             'auth_type_list': self.auth_type_list(),


        }
        return result

    def global_dict_tag(self):
        result = {}
        return result

    def delete_server(self):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(self.request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            self.data.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def put_server(self):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(self.request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                   if self.put_data:
                       self.put_data.objects.filter(id=nid).update(**row_dict)
                   else:
                       self.data.objects.filter(id=nid).update(**row_dict)
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

    def post_server(self):
        response = BaseResponse()
        add_dict = QueryDict(self.request.body, encoding='utf-8')
        data = {}
        for k, v in add_dict.items():
            data[k] = v
        obj = self.form(data)
        if obj.is_valid():
            if self.post_data:
                # for save_model in self.post_data:
                #     temp={}
                #     for i in obj.cleaned_data:
                #         for j in save_model._meta.fields:
                #             if j.name==i:
                #                 temp[i]=obj.cleaned_data['i']
                #     save_model.objects.create(**temp)
                self.post_data.objects.create(**obj.cleaned_data)

            else:
                self.data.objects.create(**obj.cleaned_data)
            response.status = True
            return response
        else:
            response.status = False
            response.data = obj.as_table()
            return response

    @staticmethod
    def idc_list():
        values = IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)

    @staticmethod
    def server_list():
        values = Server.objects.only('id', 'hostname')
        result = map(lambda x: {'id': x.id, 'name': x.hostname}, values)
        return list(result)

    @staticmethod
    def device_status_list():
        result = map(lambda x: {'id': x[0], 'name': x[1]}, Asset.device_status_choices)
        return list(result)

    @staticmethod
    def device_type_list():
        result = map(lambda x: {'id': x[0], 'name': x[1]}, Asset.device_type_choices)
        return list(result)

    @staticmethod
    def business_unit_list():
        values = BusinessUnit.objects.values('id', 'name')
        return list(values)

    @staticmethod
    def auth_type_list():
        result = map(lambda x: {'id': x[0], 'name': x[1]}, RemoteUser.auth_type_choices)
        return list(result)

