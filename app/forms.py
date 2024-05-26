from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id','product_code', 'product_name', 'product_description', 'product_quantity', 'product_status']