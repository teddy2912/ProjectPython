from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=250,null=True)
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL, null=True,blank=False)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    description = models.CharField(max_length=250,null=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=100,null=True)
    def __str__(self):
        return str(self.id)   

class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

