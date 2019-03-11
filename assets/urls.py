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

from django.urls import path,re_path
from assets.views import home
from assets.views import cmdb

app_name = "assets"

urlpatterns = [

    path('',home.CmdbView.as_view(),name="assets_index"),

    re_path('^asset/$', cmdb.AssetView.as_view(), name="asset"),
    re_path('^asset/(?P<asset_id>\d+)/$', cmdb.AssetDetailView.as_view(), name="asset_detail"),
    re_path('^assets/$', cmdb.AssetsView.as_view(), name="assets"),

    re_path('^bind_host/$', cmdb.BindHostView.as_view(), name="bind_host"),
    re_path('^bind_hosts/$', cmdb.BindHostsView.as_view(), name="bind_hosts"),

    re_path('^idc/$', cmdb.IdcView.as_view(), name="idc"),
    re_path('^idc_info/$', cmdb.IdcInfoView.as_view(), name="idc_info"),

    re_path('^tag/$', cmdb.TagView.as_view(), name="idc_info"),
    re_path('^tags/$', cmdb.TagsView.as_view(), name="idc_info"),

    re_path('^asset_log/$', cmdb.AssetLog.as_view(), name="idc_info"),
    re_path('^asset_logs/$', cmdb.AssetLogs.as_view(), name="idc_info"),



    re_path('^chart-(?P<chart_type>\w+)/$', home.ChartView.as_view()),
]

