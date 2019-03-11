from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from  django.conf import settings
import os,re,json
from eye.models import UserCmdLog
from tasks.models import Task
from tasks.backend.task_manager import  MultiTaskManger
from tasks.backend.audit import AuditLogHandler
from django.views import View


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %T")


class EyeIndex(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'eye_index.html')


def webssh(request):
    return render(request,'web_ssh.html')


class UserAudit(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        log_dirs = os.listdir(settings.AUDIT_LOG_DIR)
        return render(request, 'eye_user_audit.html', locals())


class AuditLogDetail(LoginRequiredMixin,View):
    def get(self, request,log_date,session_id, *args, **kwargs):
        log_date_path = "%s/%s" % (settings.AUDIT_LOG_DIR, log_date)
        log_file_path = "%s/session_%s.log" % (log_date_path, session_id)

        log_parser = AuditLogHandler(log_file_path)
        cmd_list = log_parser.parse()

        return render(request, "user_audit_detail.html", locals())


class AudtLogDate(LoginRequiredMixin,View):
    def get(self, request,log_date, *args, **kwargs):
        log_date_path = "%s/%s" % (settings.AUDIT_LOG_DIR, log_date)
        log_file_dirs = os.listdir(log_date_path)
        session_ids = [re.search("\d+", i).group() for i in log_file_dirs]

        session_objs = UserCmdLog.objects.filter(id__in=session_ids)

        return render(request, 'user_audit_file_list.html', locals())


def multitask_cmd(request):

    return render(request,"multitask_cmd.html")


def multitask_file_transfer(request):
    return render(request,'multitask_file_transfer.html')


def multitask_result(request):
    task_id = request.GET.get('task_id')
    task_obj = Task.objects.get(id=task_id)
    task_log_results = list(task_obj.tasklogdetail_set.values('id', 'result','status','start_date','end_date'))

    return  HttpResponse(json.dumps(task_log_results,default=json_date_handler))


def multitask(request):

    # print("--->",request.POST)
    task_data = json.loads(request.POST.get('task_data'))
    # print("--->selcted hosts",task_data)

    task_obj= MultiTaskManger(request)
    selected_hosts = list(task_obj.task.tasklogdetail_set.all().values('id', 'bind_host__host__ip_addr',
                                                             'bind_host__host__hostname', 'bind_host__remote_user__username'))
    return HttpResponse(
        json.dumps({'task_id':task_obj.task.id,'selected_hosts':selected_hosts})
    )



