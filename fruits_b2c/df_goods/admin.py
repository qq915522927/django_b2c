from django.contrib import admin
from  .models import *
# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']
#admin模型类，通过定义属性对admin界面的显示做设置
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id','gtitle','gprice','gunit','gkucun']
admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodInfo,GoodsInfoAdmin)
