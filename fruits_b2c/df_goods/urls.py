from  django.conf.urls import url
from . import views
urlpatterns = [


    url(r'^$',views.index),
    url(r'^list_(\d+)_(\d+)_(\d+)$',views.list),

]