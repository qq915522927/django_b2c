from django.db import models

# Create your models here.

class Order(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)#订单号
    user = models.ForeignKey('df_user.User')
    odate = models.DateTimeField(auto_now=True)#订单提交时间
    oisPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6,decimal_places=2)#小数为2位，一共6位
    oadress = models.CharField(max_length=150)

class OrderDetail(models.Model):
    goods = models.ForeignKey('df_goods.GoodInfo')
    order = models.ForeignKey(Order)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField()