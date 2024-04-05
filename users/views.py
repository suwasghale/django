from django.shortcuts import render,redirect
from products.models import *  # products ko models baata liney.
from django.contrib.auth.decorators import login_required
from .models import Cart,Order, User
from django.contrib import messages
from .forms import *

# Create your views here.
def index(request):
    products=Product.objects.all().order_by('-id')[:8]   # order by id descending, and limit of 8.

    context={
        'products':products
    }
    return render (request, 'users/index.html',context)  # data ya form send garnu parne vayema chai context rakhne.


def products(request):
    products=Product.objects.all().order_by('-id') #to show latest products on top.
    context={
        'products':products
    }
    return render(request, 'users/products.html',context)

def productdetails(request,product_id):
    product=Product.objects.get(id=product_id)
    context={
        'product':product
    }
    return render(request, 'users/productdetails.html',context)

@login_required
def add_to_cart(request,product_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    check_items_presence=Cart.objects.filter(user=user,product=product)
    if check_items_presence:
        messages.add_message(request,messages.ERROR,'Product is already present in the cart.')
        return redirect('/productlist')
    else:
        cart=Cart.objects.create(product=product,user=user) # aghadiko model maa vayeko and paxadiko chai mathi banako variable.
        if cart:    
            messages.add_message(request, messages.SUCCESS,'Product added to the cart.')
            return redirect('/cart')
        else:
            messages.add_message(request,messages.ERROR,'Something went wrong.')

@login_required
def show_cart_items(request):
    user=request.user
    items=Cart.objects.filter(user=user)
    context={
        'items':items
    }

    return render(request,'users/cart.html',context)


@login_required
def remove_cart_item(request,cart_id):
    item=Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, 'Item removed from the cart.')
    return redirect('/cart')


@login_required
def order_form(request,product_id,cart_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    cart_item=Cart.objects.get(id=cart_id)

    if request.method =='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            quantity=request.POST.get('quantity')
            price=product.product_price
            total_price=int(quantity) * int(price)
            contact=request.POST.get('contact')
            address=request.POST.get('address')
            payment_method=request.POST.get('payment_method')
            order=Order.objects.create(
                product=product,
                user=user, # column ko name = variable ko name
                quantity=quantity,
                contact=contact,
                total_price=total_price,
                address=address,
                payment_method=payment_method,

            )
            if order.payment_method=='Cash on Delivery':
                cart=Cart.objects.get(id=cart_id)
                cart.delete() #item order garisakesi cart bata delete hunuparyo.
                messages.add_message(request, messages.SUCCESS, 'Order Successfully!')
                return redirect('/myorder')
            elif order.payment_method=='Esewa':
                context={
                    'order': order,
                    'cart':cart_item
                }
                return render(request, 'users/esewa_payment.html',context)
            else:
                messages.add_message(request, messages.ERROR, 'Something went wrong.')
                return redirect('/cart')

    context={
        'form':OrderForm
    }
    return render(request, 'users/orderform.html',context)

import requests as req
def esewa_verify(request):
    import xml.etree.ElementTree as ET
    o_id=request.GET.get('oid')
    amount=request.GET.get('amt') #form maa vayeko 'amt'.
    refId=request.GET.get('refId')
    url="https://uat.esewa.com.np/epay/transrec"
    d = {
    'amt': amount,
    'scd': 'EPAYTEST',
    'rid': refId,
    'pid':o_id,
    }
    resp=req.post(url,d) # d=data
    root=ET.fromstring(resp.content)
    status=root[0].text.strip()
    if status =='Success': #Success ko spelling yahi hunuparxa, esewa bata yastai aauney vayekale.
        order_id=o_id.split('_')[0]
        order=Order.objects.get(id=order_id)
        order.payment_status=True
        order.save()

        cart_id=o_id.split('_')[1]
        cart=Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request, messages.SUCCESS, 'Thank you, Your Payment is successfull.')
        return redirect('/myorder')
    else:
        messages.add_message(request, messages.ERROR, ' Unable to make payment.')
        return redirect('/cart')

    
# def esewa_verify(request):
    # o_id = request.GET.get('oid')
    # amount = request.GET.get('amt')
    # refId = request.GET.get('refId')

    # if not (o_id and amount and refId):
    #     messages.add_message(request, messages.ERROR, 'Invalid or missing parameters.')
    #     return redirect('/cart')

    # order_id, cart_id = o_id.split('_', 1)  # Limit the split to one occurrence

    # try:
    #     order = Order.objects.get(id=order_id)
    #     order.payment_status = True
    #     order.save()

    #     cart = Cart.objects.get(id=cart_id)
    #     cart.delete()

    #     messages.add_message(request, messages.SUCCESS, 'Thank you, Your Payment is successful.')
    #     return redirect('/myorder')
    # except (ValueError, Order.DoesNotExist, Cart.DoesNotExist):
    #     messages.add_message(request, messages.ERROR, 'Unable to process payment.')
    #     return redirect('/cart')

@login_required
def my_order(request):
    user=request.user  #jasle login gareko xa usle matrai dekhne.
    items=Order.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request, 'users/myorder.html',context)

def profile(request):
    user = User.objects.get(username= request.user)
    context = {
        'user':user
    }
    return render(request, "users/profile.html", context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.post, instance = request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "profile updated successfully.")
            return redirect('/profile')
        else:
            messages.add_message(request, messages.ERROR, "failed to update profile.")
            return render(request, 'users/updateprofile.html', {'form':form})
    context = {
        'formss':ProfileUpdateForm(instance= request.user)
    }
    return render (request, 'users/updateprofile.html', context)