from django.shortcuts import render,redirect,HttpResponseRedirect

# Create your views here.
from django.views import View
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class IndexView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


def login_user(request):
    """
    登录
    :param request: username,password
    :return:
    """
    error_msg = "请登录"
    error_msg1 = "用户名或密码错误,或者被禁用,请重试"
    #
    # if request.method == "GET":
    #     print(request.GET.get("next"), 'ooooooooooooooo')


    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        '''czk
                user = authenticate(username=u, password=p)
        '''
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['is_login'] = True
                login_ip = request.META['REMOTE_ADDR']
                '''czk
                login_ip = request.META.get('REMOTE_ADDR','unknown')
                '''
                # LoginLogs.objects.create(user=request.user, ip=login_ip)
                print(request.META,'ooooooooooooooo')
                return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/")
            else:
                return render(request, 'login.html',
                              {'error_msg': error_msg1, })
        else:
            return render(request, 'login.html',
                          {'error_msg': error_msg1, })

    return render(request, 'login.html', {'error_msg': error_msg, })

def logout_user(request):
    """
    退出
    :param request:
    :return:
    """
    request.session.clear()
    '''-----------------------------czk-----------------
    logout(request)
    '''
    return redirect('/login/')