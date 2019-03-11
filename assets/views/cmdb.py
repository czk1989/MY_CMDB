#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from assets.service.base_server import BaseServers
from assets.models import IDC,Asset,Tag,AssetRecord,BindHost,RemoteUser
from assets.form import IdcForm,AssetForm,TagForm,BindhostForm
from assets.utils.response import BaseResponse
from django.http.request import QueryDict

class AssetView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset.html')


class AssetDetailView(LoginRequiredMixin,View):
    def get(self, request,asset_id, *args, **kwargs):
        obj = Asset.objects.filter(id=int(asset_id)).first()
        return render(request, 'asset_detail.html',locals())


class AssetsView(LoginRequiredMixin,View):
    def get(self, request):
        response = BaseServers(request,'asset',Asset,form=AssetForm).get_server()
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = BaseServers(request,'asset',Asset,form=AssetForm).post_server()
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = BaseServers(request,'asset',Asset,form=AssetForm).delete_server()
        return JsonResponse(response.__dict__)

    def put(self,request):
        response = BaseServers(request,'asset',Asset,form=AssetForm).put_server()
        return JsonResponse(response.__dict__)


class IdcView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'idc.html')


class IdcInfoView(LoginRequiredMixin,View):
    def get(self, request):
        response = BaseServers(request,'idc',IDC,form=IdcForm).get_server()
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = BaseServers(request,'idc',IDC,form=IdcForm).post_server()
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = BaseServers(request,'idc',IDC,form=IdcForm).delete_server()
        return JsonResponse(response.__dict__)

    def put(self,request):
        response = BaseServers(request,'idc',IDC,form=IdcForm).put_server()
        return JsonResponse(response.__dict__)


class TagView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tag.html')


class TagsView(LoginRequiredMixin,View):
    def get(self, request):
        response = BaseServers(request,'tag',Tag,form=TagForm).get_server()
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = BaseServers(request,'tag',Tag,form=TagForm).post_server()
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = BaseServers(request,'tag',Tag,form=TagForm).delete_server()
        return JsonResponse(response.__dict__)

    def put(self,request):
        response = BaseServers(request,'tag',Tag,form=TagForm).put_server()
        return JsonResponse(response.__dict__)


class AssetLog(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'log.html')


class AssetLogs(LoginRequiredMixin,View):
    def get(self, request):
        response = BaseServers(request,'log',AssetRecord,form=None,add=False).get_server()
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = BaseServers(request,'log',AssetRecord,form=None,add=False).post_server()
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = BaseServers(request,'log',AssetRecord,form=None,add=False).delete_server()
        return JsonResponse(response.__dict__)

    def put(self,request):
        response = BaseServers(request,'log',AssetRecord,form=None,add=False).put_server()
        return JsonResponse(response.__dict__)


class BindHostView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        # obj=BindHost.objects.select_related('host__business_unit').all()
        return render(request, 'bind_host.html')


class BindHostsView(LoginRequiredMixin,View):
    def get(self, request):
        response = BaseServers(request,'bindhost',BindHost,form=BindhostForm).get_server()
        return JsonResponse(response.__dict__)

    def post(self, request):

        response = BaseResponse()
        add_dict = QueryDict(self.request.body, encoding='utf-8')
        data = {}
        for k, v in add_dict.items():
            data[k] = v
        obj = BindhostForm(data)
        if obj.is_valid():
            asset_save=obj.cleaned_data.pop('host')
            new_remoteuser=RemoteUser.objects.create(**obj.cleaned_data)
            BindHost.objects.create(host=asset_save,remote_user=new_remoteuser)
            response.status = True
        else:
            response.status = False
            response.data = obj.as_table()
        # response = BaseServers(request,'bindhost',BindHost,form=BindhostForm,post_data=RemoteUser).post_server()
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = BaseServers(request,'bindhost',BindHost,form=None,add=False).delete_server()
        return JsonResponse(response.__dict__)

    def put(self,request):
        response = BaseServers(request,'bindhost',BindHost,form=None,add=False,put_data=RemoteUser).put_server()
        return JsonResponse(response.__dict__)