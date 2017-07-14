from django.shortcuts import render, redirect
from django.http import *
from .models import User
from df_goods.models import GoodInfo
from  hashlib import sha1
from . import user_decorator


# Create your views here.
def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    uemail = post.get('email')
    # allow = post.get('allow')
    # 判断密码是否相等
    if pwd != cpwd:
        return redirect('/user/register')
    # 密码加密
    # 使用sha1加密
    s1 = sha1()
    # sha1加密前，要先编码为比特
    s1.update(pwd.encode('utf8'))
    pwd = s1.hexdigest()
    # 存入数据库
    user = User()
    user.uname = uname
    user.upwd = pwd
    user.uemil = uemail
    user.save()
    print(user.uname)
    return redirect('/user/login')


def register_exist(request):
    uname = request.GET.get('uname')  # 通过url传参的方式
    count = User.objects.filter(uname=uname).count()
    # print(count)
    # 返回json字典，判断是存在，
    return JsonResponse({'count': count})


def login(request):

    uname = request.COOKIES.get('uname','')

    pwd = request.COOKIES.get('upwd','')

    context = {'uname': uname,
               'pwd': pwd,
               'error': 0}
    try:
        url = request.META['HTTP_REFERER']
    except:url = '/'
    response = render(request, 'df_user/login.html', context)
    # render方法返回httpesponse方法
    response.set_cookie('url', url)
    return response


def login_handle(request):
    # 接收表单数据
    post = request.POST
    uname = post.get('username')
    upwd1 = post.get('pwd')
    # 设置默认值
    remember = post.get('remember', '0')

    # 加密
    s1 = sha1()
    s1.update(upwd1.encode('utf8'))
    upwd = s1.hexdigest()
    # 验证用户是否正确
    user = User.objects.filter(uname=uname).filter(upwd=upwd).first();

    if user:

        url = request.COOKIES.get('url', '/')  # 第二个参数为默认参数，如果url没有，则条首页
        red = HttpResponseRedirect(url)
        # 如果记住密码则将用户名和密码写入cookies
        if remember == '1':

            red.set_cookie('uname', user.uname)
            red.set_cookie('upwd', upwd1)

        else:
            red.set_cookie('uname', '',max_age=-1)
            red.set_cookie('upwd', '',max_age=-1)
            # request.COOKIES['userinfo']=[user.uname,user.upwd]
        request.session['username'] = uname
        request.session['uid'] = user.id
        return red

    else:
        #如果没有用户，怎返回错误参数
        context = {'error': 1,
                   'uname': uname}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()  # 清空所有session
    return redirect('/')


@user_decorator.login
def user_center_info(request):
    username = request.session.get('username')
    user = User.objects.filter(uname=username).first()

    #获取最近浏览的商品
    goodids = request.COOKIES.get('goodids','')#获得 cookie存的记录
    goodidsl = goodids.split(',')#拆分为列表

    #这样查询可以的到所需商品，但顺序无法维护，无法为原先设定顺序
    # GoodInfo.objects.filter(id__in=goodids)
    goods_list = []#用来存放 商品列表，并维持顺序不变
    for good_id in goodidsl:
        goods = GoodInfo.objects.filter(pk=good_id).first()
        goods_list.append(goods)


    context = {'title': '用户中心', 'username': username, 'phone': user.uphone, 'adress': user.uadr,
                'good_list':goods_list}
    return render(request, 'df_user/user_center_info.html', context)

def user_center_site(request):
    username = request.session.get('username')
    user = User.objects.filter(uname=username).first()
    if request.method == 'POST':
        adr = request.POST.get('area')
        username = request.POST.get('user')
        phone = request.POST.get('phone')
        user.uadr = adr
        user.uphone =phone
        user.urelname = username
        user.save()
    context = {'adr':user.uadr,
               'user':user.urelname,
               'phone':user.uphone,}
    return render(request,'df_user/user_center_site.html',context)