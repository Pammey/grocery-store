from django.contrib import admin

# Register your models here.
from .models import Product, Category, Subscriber

admin.site.register(Subscriber)
admin.site.register(Product)
admin.site.register(Category)
