import random
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from models import *
def cart(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user
        categoryList = Category.objects.all()
        # nếu order null thì total = 0
        try:
            order = Order.objects.filter(is_paid=False, user=user).first()
            cart_items = OrderDetail.objects.filter(order=order)
            total_price = order.get_cart_total()
        except AttributeError:
            order = None
            cart_items = None
            total_price = 0
        context = {'cart_items': cart_items,
                   'total_price': total_price, 'categoryList': categoryList}
    return render(request, 'pages/cart.html', context)

def addCart(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        order, _ = Order.objects.get_or_create(user=user)
        order_details = OrderDetail.objects.filter(order=order, product=product)

        if order_details.exists():
            order_detail = order_details.first()
            order_detail.quantity += 1
            order_detail.save()
        else:
            order_detail = OrderDetail(order=order, product=product, quantity = 1)
            order_detail.save()

        # Chuyển người dùng đến trang giỏ hàng
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        note = request.POST.get('note')
        user = request.user
        order = Order.objects.filter(is_paid=False, user=user).first()
        if order:
            order.is_paid = True
            order.save()
        total = 0
        customer = ShippingAddress.objects.create(
            name=name, address=address, phone=phone, note=note, total=total)
        if customer:
            customer.user = request.user
            customer.order = order
            customer.save()
        order.customer = customer
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'app/checkout.html')

