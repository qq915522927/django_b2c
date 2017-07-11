from django.shortcuts import render,redirect
from django.http import *
from .models import User
from  hashlib import sha1
from . import user_decorator
# Create your views here.
def register(request):
    return render(request,'df_user/register.html')


def register_handle(request):
    #接收用户输入
    post = request.POST
    uname =post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    uemail = post.get('email')
    #allow = post.get('allow')
    #判断密码是否相等
    if pwd !=cpwd:
        return redirect('user/register')
    #密码加密
    #使用sha1加密
    s1 = sha1()
    #sha1加密前，要先编码为比特
    s1.update(pwd.encode('utf8'))
    pwd = s1.hexdigest()
    #存入数据库
    user = User()
    user.uname = uname
    user.upwd = pwd
    user.uemil = uemail
    user.save()
    print(user.uname)
    return redirect('user/login/')

def login(request):
    return render(request,'df_user/login.html')

def login_handle(request):
    #接收表单数据
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember')

    #加密
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd = s1.hexdigest()
    #验证用户是否正确
    user = User.objects.filter(uname=uname).filter(upwd=upwd).first();

    if user:

        url = request.COOKIES.get('url','/')#第二个参数为默认参数，如果url没有，则条首页
        red =HttpResponseRedirect(url)
        #如果记住密码则将用户名和密码写入cookies
        if remember=='on':
            pass
            request.COOKIES['userinfo']=[user.uname,user.upwd]
        request.session['username'] = uname
        request.session['pwd'] = upwd
        return red

    else:
        return HttpResponse('false')

def logout(request):
    request.session.flush()#清空所有session
    return  redirect('/')

@user_decorator.login
def user_center_info(request):
    username = request.session.get('username')
    user =User.objects.filter(uname=username).first()
    context ={'title':'用户中心','username':username,'phone':user.uphone,'adress':user.uadr}
    return render(request,'df_user/user_center_info.html',context)
