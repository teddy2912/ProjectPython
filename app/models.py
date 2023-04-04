from django.db import models
from django.contrib.auth.models import User
from model_utils.fields import StatusField
from model_utils import Choices
from django.contrib.auth.forms import UserCreationForm
# Create your models here.

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password1','password2']

class Category(models.Model):
    name = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=250,null=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    description = models.CharField(max_length=250,null=True)
    image = models.ImageField(null=True,blank=True)
    views = models.IntegerField(null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=False)

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
    code = models.CharField(max_length=5, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS = Choices('Order', 'trade', 'published', 'end', 'Canceled')
    status = StatusField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=False)  
    @property
    def get_cart_items(self):
        orderdetails = self.orderdetail_set.all()
        total = sum([item.quantity for item in orderdetails ])
        return total
    @property
    def get_cart_total(self):
        order_details = self.orderdetail_set.all()
        total_price = sum([items.get_total for items in order_details])
        return total_price
   
    
    
    
class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=10,null=True)
    note = models.CharField(max_length=1208,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True)
    def __str__(self):
        return self.address
    def get_product_price(self):
        price = [self.product.price * self.quantity]
        return sum(price)

