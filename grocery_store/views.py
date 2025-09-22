from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'shop.html')
def product_detail(request):
    return render(request, 'product_details.html')
