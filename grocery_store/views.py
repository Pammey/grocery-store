from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subscriber
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def home(request):
    return HttpResponse("Hello, this is my new app!")
# Create your views here.

def homepage(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# @login_required(login_url='/account/login/')
def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_slug = request.GET.get("category")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    search_query = request.GET.get("search")

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    max_price = request.GET.get("max_price")

    if max_price:
       products = products.filter(price__lte=max_price)

    sort = request.GET.get("sort")

    if sort == "price_low":
      products = products.order_by("price")

    elif sort == "price_high":
                products = products.order_by("-price")

    elif sort == "name":
      products = products.order_by("name")

    else:
     # Default: newest products first
        products = products.order_by("-created_at")

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "page_obj": page_obj,
        "search_query": search_query,
        "selected_category": category_slug,
        "sort": sort,
        "max_price": max_price,
    }
    return render(request, "shop.html", context)
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    return render(request, "product_details.html", {
        "product": product,
        "related_products": related_products,
    })
def sign_in(request):
    """Renders the sign-in/sign-up page."""
    return render(request, 'sign-in.html')

def subscribe(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Only POST requests are allowed."
        }, status=405)

    email = request.POST.get("email", "").strip()

    if not email:
        return JsonResponse({
            "status": "error",
            "message": "Please enter an email address."
        }, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "status": "error",
            "message": "Please enter a valid email address."
        }, status=400)

    subscriber, created = Subscriber.objects.get_or_create(email=email)

    if created:
        return JsonResponse({
            "status": "success",
            "message": "Thanks for subscribing!"
        })

    return JsonResponse({
        "status": "info",
        "message": "You're already subscribed."
    })