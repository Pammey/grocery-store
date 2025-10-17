# orders/forms.py

from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'state']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+234...'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Fresh Avenue'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ikeja'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lagos'}),
        }