from django.db import models

# Create your models here.

class User(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemil = models.CharField(max_length=30)
    urelname =models.CharField(max_length=20,default='')
    uadr = models.CharField(max_length=100,default='')
    uphone = models.CharField(max_length=11,default='')

