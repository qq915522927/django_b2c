from django.shortcuts import render
from .models import *


# Create your views here.


def index(request):
    context = {'guest_cart': 1,
               'title': '首页'}

    #获得最新火的4 个 商品
    hot = GoodInfo.objects.all().order_by('-gclick')[0:4]
    context.setdefault('hot',hot)

    #****获得各分类下的点击商品************
    # 先获得所有分类
    typelist = TypeInfo.objects.all()
    for i in range(len(typelist)):
        # 获得type对象
        type = typelist[i]
        # 根据type对象获取商品列表
        # 通过外键关联获取商品
        # 获取 对应 列表中的通过 id 倒序排列的 前四个
        goods1 = type.goodinfo_set.order_by('-id')[0:4]
        goods2 = type.goodinfo_set.order_by('-gclick')[0:4]
        key1 = 'type' + str(i)  # 根据id 倒叙排列
        key2 = 'type' + str(i) + str(i)  # 根据点击量倒序排列
        context.setdefault(key1, goods1)
        context.setdefault(key2, goods2)
    print(context)
    return render(request, 'df_goods/index.html', context)



#商品列别界面，要接受多个参数
#1，type id
#2. 排序 的方式
#3. 分页的页码
def list(request,tid,sid,pindex):
    from django.core.paginator import Paginator,Page

    type = TypeInfo.objects.get(pk=int(tid))
    news = type.goodinfo_set.order_by('-id')[0:2]
    if sid == '1':
        good_list = type.goodinfo_set.order_by('-id')#按时间最新的排列
    if sid == '2':
        good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')#按价格
    if sid == '3':
        good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    #创建paginator分页对象
    paginator = Paginator(good_list,10)
    #返回Page对象,包含商品信息
    page = paginator.page(int(pindex))

    context = {'title':'商品列表',
               'guest_cart':1,
               'page':page,
               'paginator':paginator,
               'typeinfo':type,
               'sort':sid,#排序方式
               'news':news,



                }

    return render(request,'df_goods/list.html',context)

def detail(request,id):
    goods = GoodInfo.objects.filter(pk=int(id)).first()
    goods.gclick += 1 #点击量加1
    goods.save()
    from df_cart.models import Cart
    #返回用于显示购物车内商品总数
    cart_count = Cart.objects.filter(user_id=request.session.get('uid',0)).count()
    news = goods.gtype.goodinfo_set.order_by('-id')[0:2]
    context = {'title':goods.gtype.ttitle,
               'goods':goods,
                'cart_count':cart_count,
               'news':news,
               'guest_cart':1,
               'typeinfo':goods.gtype
               }
    response = render(request,'df_goods/detail.html',context)

    #接下来，要将浏览信息，存入 cookie ，以便 最近浏览 功能使用
    #存入 cookie 的形式微 { 'gooids':'1,5,6,7,8,9'}
    #id间已逗号隔开
    goodids = request.COOKIES.get('goodids','')
    if goodids != '':
        goodidsl = goodids.split(',') #将字符串 拆分成 列表
        if goodidsl.count(id) >=1 :#先判断 是否已经存在列表里
            #如果已经存在，则删除存在的元素,之后会插入新的
            goodidsl.remove(id)
        #将新的id放在 列表的 第一个
        goodidsl.insert(0,id)
        if len(goodidsl) >=6:#如果超过 6个，则删除最后一个，相当于长度为5的队列
            del goodidsl[5]
        goodids = ','.join(goodidsl)#将列表，以逗号分割的形式 拼接为字符串
    else:#如果为空则 直接 添加
        goodids = id


    response.set_cookie('goodids',goodids)

    return  response
