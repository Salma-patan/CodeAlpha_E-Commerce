from django import forms
from .models import Product, Order
from django.utils.text import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock', 'image', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full shipping address'}),
        label='Shipping Address'
    )
    phone = forms.CharField(
        max_length=15,
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': '+91 9876543210'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any special delivery instructions...'}),
        label='Order Notes (Optional)'
    )
