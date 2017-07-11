from django.http import *
#验证session中是否有用户

def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('username'):
            #如果成功登录，继续执行 原函数
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            #将当前页的url存入cookie

            red.set_cookie('url',request.get_full_path())

            return red
    return login_fun