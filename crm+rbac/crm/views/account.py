from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from django.conf import settings
from rbac.service.permission import init_permisson


def login(request):
    err_msg = ''
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
        if not obj:
            err_msg = '用户名或密码错误'
        else:
            # 登录成功
            # 记录权限的信息
            init_permisson(request, obj)
            return redirect(reverse('index'))

    return render(request, 'login.html', {'err_msg': err_msg})
