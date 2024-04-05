from django.shortcuts import render,redirect
from .models import Product,Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.auth import admin_only
# Create your views here.
@login_required
@admin_only
def index(request):
    # fetch data from the table 
    products=Product.objects.all() # product maa vayeko sabai data fetch gara
    context={
        'products':products
    }
    return render(request,'products/products.html',context)  # page load garda request, kun page maa dekhauney, ani k dekhauney.

@login_required
@admin_only
def post_product(request):
     if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Product Added.')
            return redirect('/products') 
        # render maa page ko name, redirect maa url diney always.
        else:
            messages.add_message(request,messages.ERROR,'Failed to add product.')
            return render (request,'products/addproduct.html',{'form':form}) # ProductForm maathi form variable maa assign gareko
       
     context={
            'form':ProductForm
        }
     return render(request,'products/addproduct.html',context)

@login_required
@admin_only
def update_product(request,product_id):
    instance=Product.objects.get(id=product_id) # eauta matrai lina lai id rakheko. product_id vaneko url baata aauxa, id chai product ko model maa hunxa.
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES, instance=instance) # particular instance matrai update huna, left ko predefined, right ko mathiko variable.
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Product updated.')
            return redirect('/products') 
        # render maa page ko name, redirect maa url diney always.
        else:
            messages.add_message(request,messages.ERROR,'Failed to update product.')
            return render (request,'products/updateproduct.html',{'form':form}) # ProductForm maathi form variable maa assign gareko
       
    context={
            'form':ProductForm(instance=instance)
        }
    return render(request,'products/updateproduct.html',context)
@login_required
@admin_only
def delete_product(request, product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    messages.add_message(request,messages.SUCCESS, ' Product Deleted.')
    return redirect('/products')


@login_required
@admin_only
def post_category(request):
     if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Category Added.')
            return redirect('/products/categories') 
        # render maa page ko name, redirect maa url diney always.
        else:
            messages.add_message(request,messages.ERROR,'Failed to add category.')
            return render (request,'products/addcategory.html',{'form':form}) # CategoryForm maathi form variable maa assign gareko
       
     context={
            'form':CategoryForm
        }
     return render(request,'products/addcategory.html',context)
@login_required
@admin_only
def show_category(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'products/categories.html/',context)

@login_required
@admin_only
def update_category(request,category_id):
    instance=Category.objects.get(id=category_id)
    if request.method == 'POST':
        form=CategoryForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category Updated.')
            return redirect('/products/categories')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to update Category.')
            return render(request, 'products/updatecategory.html',{'form':form})
        
    context={
        'form':CategoryForm(instance=instance)
    }
    return render(request, 'products/updatecategory.html',context)

@login_required
@admin_only
def delete_category(request,category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS,'Category Deleted.')
    return redirect('/products/categories')