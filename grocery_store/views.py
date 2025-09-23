from django.shortcuts import render
from django.http import HttpResponse
from.models import Product, Category

def home(request):
    return HttpResponse("Hello, this is my new app!")
# Create your views here.

def homepage(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    return render(request, 'shop.html', {'categories': categories, 'products': products})
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'product_details.html', {'product': product})
