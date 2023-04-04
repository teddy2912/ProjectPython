from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name ='app'
urlpatterns= [
    path('', home,name="home"), 
    path('register/', register,name="register"),
    path('login/', loginPage,name="login"),
    path('logout/', logoutPage,name="logout"),
    path('cart/', cart,name="cart"), 
    path('checkout/', checkout,name="checkout"), 
    path('viewCartcheckout/', viewCartcheckout, name='viewCartcheckout'),
    path('product_detail/<int:id>', product_detail,name="product_detail"), 
    path('contact/', contact,name="contact"), 
    path('update_item/', updateItem,name="update_item"), 
    path('addCart/<int:product_id>/', addCart, name='addCart'),
    path('removeCart/<int:id>',removeCart, name='removeCart' ),
    # path('updateCart-cart/<int:id>',updateCart, name='updateCart'),
    path('checkout/', checkout, name='checkout'),
]