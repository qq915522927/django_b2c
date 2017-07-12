from django.shortcuts import render


# Create your views here.


def index(request):
    context = {'guest_cart':1,
               'title':'首页'}
    return  render(request,'df_goods/index.html',context)