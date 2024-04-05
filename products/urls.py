# file ko name same hunuparxa main project folder ko jastai.

from django.urls import path

from .views import *
# from . import views -2

urlpatterns=[
 path('',index),
 path('addproduct/',post_product),
 path('updateproduct/<int:product_id>',update_product), # product_id from views.
 path('deleteproduct/<int:product_id>',delete_product),
 
 path('addcategory/',post_category),
 path('categories/',show_category),
 path('categories/updatecategory/<int:category_id>',update_category),
 path('categories/deletecategory/<int:category_id>',delete_category),
]