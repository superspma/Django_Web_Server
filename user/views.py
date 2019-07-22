from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import models


# Create your views here.


def login_view(request):
    if 'user' in request.session:
        print('用户已登录！！！')
    else:
        print("用户没登录！")
    # value = request.session.get('mypassword', '没有设置密码')
    # print('密码是：' + value)
    if request.method == "GET":
        username = request.COOKIES.get('myname', '')
        return render(request, 'user/login.html', locals())
    elif request.method == "POST":
        username = request.POST.get('username', '')
        if username == '':
            # 表单验证（验证用户提交的数据是否合法）
            name_error = "请填写用户名！！！"
            return render(request, 'user/login.html', locals())
        password = request.POST.get('password', '')
        # request.session['mypassword'] = password
        remember = request.POST.get('remember', '0')

        # 进行登录逻辑操作
        try:
            auser = models.User.objects.get(
                username=username, password=password)
        except:
            password_error = '用户名或密码不正确'
            return render(request, 'user/login.html', locals())
        # 如果能走到此处，说明用户名密码正确
        # 在session中表示当前用户是的登录状态
        request.session['user'] = {
            'name': auser.username,
            'id': auser.id
        }
        # resp = HttpResponse('提交成功！<a href="/"> 进入主页</a>') #remember= ' + remember)
        resp = HttpResponseRedirect('/')
        if remember == '1':
            resp.set_cookie('myname', username, max_age=7 * 24 * 60 * 60)
        else:
            resp.delete_cookie('myname')

        return resp


def logout_view(request):
    # 退出登录；
    if 'user' in request.session:
        del request.session['user']
    # 返回主页
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('/')


def reg_view(request):
    if request.method == "GET":
        return render(request, 'user/reg.html', locals())
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        if username == '':
            name_error = '请填写用户名！！！'
            return render(request, 'user/reg.html', locals())
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if password != password2:
            password2_error = '两次输入的的密码不一致！！！'
            return render(request, 'user/reg.html', locals())
        try:
            a_user = models.User.objects.get(username=username)
            name_error = '该用户已存在！！！'
            return render(request, 'user/reg.html', locals())
        except:
            pass
            # 添加用户数据，完成注册
        a_user = models.User.objects.create(
            username=username,
            password=password
        )
        html = username + '注册成功！！！<a href="/user/login"> 进入登录</a>'
        return HttpResponse(html)


from . import forms


def reg2_view(request):
    if request.method == "GET":
        reg2 = forms.Reg2()
        return render(request, 'user/reg2.html', locals())
    elif request.method == "POST":
        # 如何拿到表单数据
        # 方法一
        # request.POSST
        username=request.POST.get('username','')
        # 方法二
        form = forms.Reg2(request.POST)
        if form.is_valid():
            html = str(form.cleaned_data)
            return HttpResponse(html)
        else:
            return HttpResponse("您提交的数据不合法！！！")
