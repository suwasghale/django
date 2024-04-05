from django.forms import ModelForm
from .models import *

class ProductForm(ModelForm):
    class Meta: # kasto kun type ko data pathauney vanera
        model=Product
        fields='__all__' # sabai field pathaideu. eauta eauta garna list/array banauney.
        
class CategoryForm(ModelForm):
    class Meta:
        model=Category
        fields='__all__'
