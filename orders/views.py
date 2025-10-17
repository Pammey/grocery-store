# orders/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save() # Save the Order instance to get an ID

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item.product,
                                         price=item.price,
                                         quantity=item.quantity)
            # Clear the cart
            cart.clear()

            # Here you would typically redirect to a payment gateway
            # For now, we redirect to a success page
            request.session['order_id'] = order.id # Store order id in session
            return redirect(reverse('orders:order_created'))

    else:
        form = OrderCreateForm()

    return render(request,
                  'checkout.html',
                  {'cart': cart, 'form': form})

def order_created(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id) if order_id else None
    return render(request, 'order_created.html', {'order': order})