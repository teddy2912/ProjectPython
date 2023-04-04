from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
import json
# from .form import UpdateCartItemForm

# Create your views here.


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'app/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or pass not correct')

    context = {}
    return render(request, 'app/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def home(request):
    # if request.user.is_authenticated:
    #     customer = request.user
    #     order, created = Order.objects.get_or_create(
    #     customer=customer)
    #     details = order.orderdetail_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     details = []
    #     order = {'get_cart_items': 0, 'get_cart_total': 0}
    #     cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/home.html',context)


def cart(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user
        categoryList = Category.objects.all()
        # nếu order null thì total = 0
        try:
            order = Order.objects.filter( user=user).first()
            cart_items = OrderDetail.objects.filter(order=order)
            total_price = order.get_cart_total
            items = order.get_cart_items
            detail_total = OrderDetail.get_total
            # print(order.get_cart_total())
        except AttributeError:
            
            order = None
            cart_items = None
            total_price = 0
        context = {'cart_items': cart_items,
                   'total_price': total_price, 'categoryList': categoryList,'items':items,'detail_total':detail_total}
    return render(request, 'app/cart.html', context)

def addCart(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user
        product = get_object_or_404(Product, id=product_id)
       
        product.save()
        order, _ = Order.objects.get_or_create(user=user)
        order.save()
        order_details = OrderDetail.objects.filter(order=order, product=product)
        if order_details.exists():
            order_detail = order_details.first()
            order_detail.quantity += 1
            order_detail.save()
        else:
            
            order_detail = OrderDetail(order=order, product=product, quantity = 1)
            order_detail.save()
            
        # Chuyển người dùng đến trang giỏ hàng
        return redirect('/cart')

# def updateCart(request, id):
#     cart_items = get_object_or_404(OrderDetail, id=id)
#     product = (Product)
#     form = UpdateCartItemForm(request.POST or None, instance=cart_items)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
#     product.quantity =+- cart_items.quantity
#     product.save()
#     context = {'form': form, 'cart_items': cart_items ,'product': product}
#     return render(request, 'app/cart.html', context)

def removeCart(request, id):
    try:
       
        order_detail = OrderDetail.objects.get(id = id)
        
        order_detail.delete()
    except Exception as e:
       
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# def cart(request):
#     if request.user.is_authenticated:
#         customer = request.user
#         order, created = Order.objects.get_or_create(customer=customer,complete=False)
#         details = order.orderdetail_set.all()
#         cartItems = order.get_cart_items

#     else:
#         details = []
#         order = {'get_cart_items':0,'get_cart_total':0}
#         cartItems = order['get_cart_items']
#     context={'details':details,'order':order,'cartItems':cartItems}
#     return render(request,'app/cart.html',context)


# def checkout(request):
#     if request.user.is_authenticated:
#         customer = request.user
#         order, created = Order.objects.get_or_create(customer=customer,complete=False)
#         details = order.orderdetail_set.all()
#         cartItems = order.get_cart_items

#     else:
#         details = []
#         order = {'get_cart_items':0,'get_cart_total':0}
#         cartItems = order['get_cart_items']
#     context={'details':details,'order':order,'cartItems':cartItems}
#     return render(request,'app/checkout.html',context)


def viewCartcheckout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user
        categoryList = Category.objects.all()
        # nếu order null thì total = 0
        try:
            order = Order.objects.filter(is_paid=False, user=user).first()
            cart_items = OrderDetail.objects.filter(order=order)
            total_price = order.get_cart_total
        except AttributeError:
            order = None
            cart_items = None
            total_price = 0
        context = {'cart_items': cart_items, 'total_price': total_price,'categoryList':categoryList}
    return render(request, 'app/checkout.html', context)


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


def product_detail(request, id):
    product_detail = Product.objects.get(id=id)
    product_detail.views += 1
    product_detail.save()
    listcategory = Category.objects.all()
    # categoryall = Product.objects.filter( categoryId = productdetails.categoryId).exclude(id = productdetails.id)[:4]
    # , 'categoryall' :categoryall
    return render(request, 'app/product_detail.html', {'product_detail': product_detail, 'category': listcategory})


def contact(request):
    context = {}
    return render(request, 'app/contact.html', context)




def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderDetail.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('added', safe=False)
