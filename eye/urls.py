"""MY_CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from eye import views

app_name='eye'
urlpatterns = [

    re_path('^$', views.EyeIndex.as_view(),name='eye_index'),
    re_path('^user_audit/$', views.UserAudit.as_view(), name="user_audit"),
    re_path('^audit_log/(\w+-\w+-\w+)/$', views.AudtLogDate.as_view(), name="audit_log_date"),
    re_path('^audit_log/(\w+-\w+-\w+)/(\d+)/$', views.AuditLogDetail.as_view(), name="audit_log_detail"),
    re_path('^webssh/$', views.webssh, name="webssh"),
    re_path('^multitask/cmd/$', views.multitask_cmd, name="multitask_cmd"),
    re_path('^multitask/file_transfer/$', views.multitask_file_transfer, name="multitask_file_transfer"),
    re_path('^multitask/$', views.multitask, name="multitask"),
    re_path('^multitask/result/$', views.multitask_result, name="task_result"),


]
