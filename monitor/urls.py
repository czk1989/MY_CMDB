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
from django.urls import path,re_path,include
from monitor import views

app_name='monitor'

urlpatterns = [
    re_path('^$', views.MonitorIndex.as_view(),name='monitor_index'),
    re_path('^triggers/$',views.triggers,name='triggers' ),
    # re_path('^api/$',include('monitor.api_urls')),
    re_path('^trigger_list/$',views.trigger_list ,name='trigger_list'),
    re_path('^hosts/$',views.hosts ,name='hosts'),
    re_path('^hosts/(\d+)/$',views.host_detail ,name='host_detail'),
    re_path('^host_groups/$',views.host_groups ,name='host_groups'),
]
