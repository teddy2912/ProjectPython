from django.shortcuts import render
from django.http import HttpRequest
from .models import *
# Create your views here.
def home(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'app/home.html',context)
# def cart(request):
#     context={}
#     return render(request,'app/home.html',context)
# def checkout(request):
#     context={}
#     return render(request,'app/home.html',context)