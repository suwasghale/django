from django.db import models
# NOTE: model maa change garne bittikai migration garnaiparxa.
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=100, unique=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.category_name


class Product(models.Model): # models baata Model import gareko
    # class vitra attribute define garda self lekhnupardaina, function vitra chai parxa
    product_name=models.CharField(max_length=100)
    product_price=models.FloatField()
    stock=models.IntegerField()
    product_description=models.TextField()
    product_image=models.FileField(upload_to='static/uploads', null=True) # kunai pani field db maa pathaunu xaina vaney null=True.
    created_date=models.DateTimeField(auto_now_add=True)
    
    category=models.ForeignKey(Category,on_delete=models.CASCADE , null=True) # category delete vayo vane product pani sangsangai delete hunuparyo.
    
    def __str__(self):
        return self.product_name