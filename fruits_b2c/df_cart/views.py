from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from df_user import user_decorator


# Create your views here.

@user_decorator.login
def cart(request):
    uid = request.session.get('uid')
    carts = Cart.objects.filter(user_id=uid)

    context = {'title': '购物车',
               'name': 1,
               'carts': carts}
    return render(request, 'df_cart/cart.html', context)

@user_decorator.login
def add(request,gid,gcount):
    gid = int(gid)
    gcount = int(gcount)
    uid = request.session.get('uid')
    carts = Cart.objects.filter(goods_id=gid,user_id=uid)
    #先判断 该用户 购物车中 是否 存在 该商品
    #如果纯在，则仅作数量上的 加法
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += gcount
    else:
        cart = Cart()
        cart.user_id = uid
        cart.goods_id =gid
        cart.count =gcount
    cart.save()
    #判断请求方式 是否是ajax，若是则返回json格式的 商品数量即可
    if request.is_ajax():
        count = Cart.objects.filter(user_id=uid).count()
        return JsonResponse({'count':count})
    else:
        return  redirect('/cart')


def edit(request,cid,gcount):#传入 cart id 和 count 改变Cart
    try:
        cart = Cart.objects.get(pk=int(cid))
        cart.count = int(gcount)
        cart.save()
    except:
        return JsonResponse({'count':gcount})

    return JsonResponse({'count':0})

def delete(request,cid):
    try:
        cart=Cart.objects.get(pk=int(cid))
        cart.delete()
        data ={'ok':1}
    except:
        data={'ok':0}
    return JsonResponse(data)