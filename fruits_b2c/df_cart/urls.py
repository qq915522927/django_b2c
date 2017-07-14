from django.conf.urls import  url
from . import  views
urlpatterns = [

    url(r'^$',views.cart),
    url(r'^add_(\d+)_(\d+)$',views.add),#第一个为 商品id，第二个为商品 数量
    url(r'^edit_(\d+)_(\d+)$',views.edit),
    url(r'^delete/(\d+)$',views.delete),

]