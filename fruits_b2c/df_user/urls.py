from django.conf.urls import url
from . import views
urlpatterns =[
    url(r'^register$',views.register),
    url(r'^register_handle$',views.register_handle),
    url(r'^login$',views.login),
    url(r'^login_handle$',views.login_handle),
    url(r'^user_center_info$',views.user_center_info),
    url(r'^logout$',views.logout),
]