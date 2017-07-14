from django.db import models

# Create your models here.
#用户 与 商品的 联系 是多对多的
#购物车 充当中间 环节，与 用户 一对多，同时 与 商品一对多

class Cart(models.Model):
    user = models.ForeignKey('df_user.User')
    goods = models.ForeignKey('df_goods.GoodInfo')
    count = models.IntegerField()
