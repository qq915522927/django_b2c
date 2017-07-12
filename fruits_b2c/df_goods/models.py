from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

class GoodInfo(models.Model):
    gtitle = models.CharField(max_length=50)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20,default='500g')
    gclick = models.IntegerField()#点击量
    gintro = models.CharField(max_length=100)#简介
    gdetial = HTMLField()
    gtype = models.ForeignKey("TypeInfo")
    # gadv = models.BooleanField(default=False)#推荐 广告商品
