from django.shortcuts import render

# Create your views here.
#_*_coding:utf8_*_
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from  django.conf import settings
import json,time
# Create your views here.
from  monitor.serializer import  ClientHandler,get_host_triggers
import json
from monitor.backends import redis_conn
from monitor.backends import data_optimization
from monitor import models
from monitor.backends import data_processing
from monitor import serializer
from monitor import graphs
from django.views import View

from assets.models import BusinessUnit

REDIS_OBJ = redis_conn.redis_conn(settings)


class MonitorIndex(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'minitor_index.html')


def triggers(request):

    return render(request,'triggers.html')


def hosts(request):
    host_list = models.MonitorHost.objects.all()
    # print("hosts:",host_list)
    return render(request,'host.html',locals())


def host_detail(request,host_id):
    host_obj = models.MonitorHost.objects.get(id=host_id)
    alert_list = host_obj.eventlog_set.all().order_by('-date')
    return render(request,'host_detail.html',locals())







def trigger_list(request):

    host_id = request.GET.get("by_host_id")

    host_obj = models.MonitorHost.objects.get(id=host_id)

    alert_list = host_obj.eventlog_set.all().order_by('-date')
    return render(request,'trigger_list.html',locals())


def host_groups(request):

    host_groups = models.MonitorHostGroup.objects.all()
    return render(request,'host_groups.html',locals())