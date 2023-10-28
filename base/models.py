from django.db import models
import datetime
import os
# Create your models here.

def getFilename(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads',new_filename)

class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFilename,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=getFilename,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class user(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    cpassword=models.CharField(max_length=100)
    contact=models.IntegerField()

class Cart(models.Model):
    prod=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    overallprice=models.IntegerField(null=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    updated=models.DateTimeField(auto_now=True)

class Buyproduct(models.Model):
    prod=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    overallprice=models.IntegerField(null=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    updated=models.DateTimeField(auto_now_add=True)
    confirm=models.BooleanField(default=False)
    delivery=models.CharField(max_length=50)
