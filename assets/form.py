from django import forms
from django.forms import fields
from django.forms import widgets
from assets.models import IDC
from assets.models import BusinessUnit,Asset,RemoteUser
from django.core.exceptions import ValidationError


class AssetForm(forms.Form):
    device_type_id = forms.CharField(initial=1,widget=widgets.Select(choices=((1, '服务器'),(2, '交换机'),(3, '防火墙'),),),label='资产类型')
    device_status_id = forms.ChoiceField(choices=((1, '上架'),(2, '在线'),(3, '离线'),(4, '下架'),),widget=widgets.Select,label='资产状态')
    cabinet_num=forms.CharField(max_length=30,label='机柜号',required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})
    cabinet_order = forms.CharField(label='机柜中序号', max_length=30,required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})
    idc = forms.models.ModelChoiceField(queryset=IDC.objects.all(),label='IDC',to_field_name="name")
    business_unit = forms.models.ModelChoiceField(queryset=BusinessUnit.objects.all(),label='业务线',to_field_name="name")

    def clean_device_type_id(self):
        device_type_id = self.cleaned_data['device_type_id']

        if int(device_type_id) not in [1,2,3]:

            raise ValidationError('请选择正确选项', 'invalid')
        return device_type_id

    def clean_device_status_id(self):
        device_status_id = self.cleaned_data['device_status_id']
        if int(device_status_id) not in [1,2,3,4]:
            print('ok')
            raise ValidationError('请选择正确选项', 'invalid')
        return device_status_id

    def clean_business_unit(self):
        business_unit=self.cleaned_data['business_unit']
        if not BusinessUnit.objects.filter(name=business_unit).first():
            raise ValidationError('请选择正确选项', 'invalid')
        return business_unit

    def clean_idc(self):
        idc=self.cleaned_data['idc']
        if not IDC.objects.filter(name=idc).first():
            raise ValidationError('请选择正确选项', 'invalid')
        return idc


class IdcForm(forms.Form):

    name=forms.CharField(max_length=30,label='机房',required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})
    floor = forms.CharField(label='楼层', max_length=30,required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})


class TagForm(forms.Form):

    name=forms.CharField(max_length=30,label='标签',required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})


class BindhostForm(forms.Form):
    username=forms.CharField(max_length=30,label='用户名',required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})
    auth_type = fields.ChoiceField(choices=((0, 'password'), (1, 'key'),),initial=2,widget=widgets.RadioSelect)
    password=forms.CharField(max_length=64,label='密码',required=True,error_messages={'required': '不能为空', 'invalid': '格式错误'})
    host = forms.models.ModelChoiceField(queryset=Asset.objects.all(), label='资产',to_field_name="id",error_messages={'required': '不能为空', 'invalid': '格式错误'})
