from django.shortcuts import render,redirect
from df_user.user_decorator import  login
from  df_cart.models import Cart
from df_user.models import User
from .models import *
from datetime import  datetime
from django.db import transaction
from decimal import Decimal
from django.http import HttpResponse
# Create your views here.
@login
def order(request):
    uid = request.session.get('uid')
    user = User.objects.get(id = uid)#获得用户对象 信息

    cartids = request.GET.getlist('cart_id')#获取多个 同名的参数
    carts = []#取出对应的所有cart对象
    totalprice = 0
    for cid in cartids:
        cart = Cart.objects.get(id=cid)
        carts.append(cart)
        totalprice = totalprice + float(cart.count) * float(cart.goods.gprice)
        totalprice = float('%0.2f'%totalprice)

    context = {'user':user,
               'carts':carts,
               'total_price':totalprice}



    return render(request,'df_order/place_order.html',context)


'''
这些步骤中，任何一环节出错都不允许，要使用 事务 提交
1. 创建订单对象
2. 判断商品 库存 充足
3. 创建 订单 详情 ，多个
4， 修改 库存
5. 删除购物车
'''

@transaction.atomic()
@login
def order_handle(request):
    tran_id = transaction.savepoint()#保存点，回退到这里
    cart_ids=request.POST.get('cart_ids')#取得购物车

    #从这里开始为一个事物，任何一环节出错，都会 回退
    try:
        # 创建订单
        order = Order()
        now = datetime.now()
        uid = request.session['uid']
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)#时间和uid组成订单号
        order.odate=now
        order.user_id = int(uid)
        order.ototal = Decimal(request.POST.get('total'))#感觉从客户端 传来总价格 不安全，应该再次计算得出来
        order.save()

        for cartid in cart_ids.split(','):
            cart = Cart.objects.get(pk=cartid)

            detail = OrderDetail()
            detail.order = order#将详情 与 订单绑定

            goods = cart.goods
            #判断商品的数量 是否大于内存
            if cart.count <= goods.gkucun:#库存充足
                #减少 商品库存
                goods.gkucun -= cart.count
                goods.save()
                #将购物车 里的东西写入到 订单详情 页
                detail.goods = goods
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                #删除购物车数据
                cart.delete()
            else:#库存不足
                transaction.savepoint_rollback(tran_id)#会滚到点
                return HttpResponse('false')

    except Exception as e:
        print('**********************%s'%e)
        transaction.savepoint_rollback(tran_id)#任何一环节出错，之前 干的事全部撤销
        return HttpResponse('false')
    else:
        transaction.savepoint_commit(tran_id)#没发生异常，提交事务
    return HttpResponse('ok')