from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import models
from user.models import User


# 写一个函数装饰器，检查用户是否登录，如果没有登录，则直接进入login
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'user' not in request.session:
            # 检查用户是否登录，如果没有登录，进入登录页面
            return HttpResponseRedirect('/user/login')
        else:
            return fn(request, *args, **kwargs)

    return wrap


# Create your views here.

def add_view(request):
    if 'user' not in request.session:
        # 检查用户是否登录，如果没有登录，进入登录页面
        return HttpResponseRedirect('/user/login')
    if request.method == "GET":
        return render(request, 'note/add_note.html')
    elif request.method == "POST":
        # 根据登陆的用户id 找到此用户
        try:
            a_user = User.objects.get(
                id=request.session['user']['id'])
        except:
            return HttpResponse('登录用户数据错误！')

        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        # 根据表单内容创建数据记录

        models.Note.objects.create(
            title=title,
            content=content,
            user=a_user
        )
        return HttpResponseRedirect('/note/')


from django.core.paginator import Paginator


@check_login
def list_view(request):
    # 检查用户是否已登录，如果没有登录则进入login
    try:
        a_user_id = request.session['user']['id']
        a_user = User.objects.get(id=a_user_id)
    except:
        return HttpResponse('数据获取失败')
    notes = a_user.note_set.all()  # 获取当前用户的所有笔记
    # return render(request, 'note/list_note.html', locals())
    paginator = Paginator(notes, 5)
    # print('分页前的数据个数',paginator.count)
    # print('当前的数据页数',paginator.num_pages)
    # print('当前对象的面码范围是:', paginator.page_range)
    # 先获取当前页码信息，如果没有page=X，返回第一页信息
    page_number = request.GET.get('page', 1)
    page = paginator.page(page_number)
    # print(page.number)
    return render(request, 'note/list_note2.html', locals())


@check_login
def del_view(request, id):
    # 先得到当前用户信息
    try:
        a_user_id = request.session['user']['id']
        a_user = User.objects.get(id=a_user_id)
    except:
        return HttpResponse('数据获取失败')
    a_note = a_user.note_set.get(id=id)
    a_note.delete()
    return HttpResponseRedirect('/note/')


@check_login
def mod_view(request, id):
    # 先得到当前用户信息
    try:
        a_user_id = request.session['user']['id']
        a_user = User.objects.get(id=a_user_id)
    except:
        return HttpResponse('数据获取失败')
    a_note = a_user.note_set.get(id=id)
    if request.method == "GET":
        return render(request, 'note/mod_note.html', locals())
    elif request.method == "POST":
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        # 修改对应的数据
        a_note.title = title
        a_note.content = content
        a_note.save()
        return HttpResponseRedirect('/note/')
