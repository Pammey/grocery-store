# cart/cart.py
from decimal import Decimal
from django.conf import settings
from grocery_store.models import Product  # Assumes your Product model is in a 'shop' app
from .models import Cart as CartModel, CartItem

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        self.user = request.user

        if self.user.is_authenticated:
            # For authenticated users, use the database cart
            cart, created = CartModel.objects.get_or_create(user=self.user)
            self.cart = cart
            # If there's a session cart, merge it with the DB cart
            session_cart = self.session.get(settings.CART_SESSION_ID)
            if session_cart:
                for product_id, item_data in session_cart.items():
                    product = Product.objects.get(id=product_id)
                    self.add(product, item_data['quantity'], override_quantity=False)
                # Clear the session cart after merging
                del self.session[settings.CART_SESSION_ID]
                self.save()
        else:
            # For anonymous users, use the session
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        price = product.get_display_price

        if self.user.is_authenticated:
            cart_item, created = self.cart.items.get_or_create(
                product=product,
                defaults={'price': price, 'quantity': quantity}
            )
            if not created:
                if override_quantity:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.price = price # Update price in case it changed
                cart_item.save()
        else:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(price)}
            
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['price'] = str(price)

        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        if not self.user.is_authenticated:
            self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if self.user.is_authenticated:
            self.cart.items.filter(product_id=product_id).delete()
        elif product_id in self.cart:
             del self.cart[product_id]
             self.save()

    def __iter__(self):
        """
        Loop through cart items and get the products from the database.
        """
        if self.user.is_authenticated:
            # Eager load products to avoid N+1 queries
            cart_items = self.cart.items.select_related('product')
            for item in cart_items:
                item.total_price = item.get_cost()
                yield item
        else:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart = self.cart.copy()
            for product in products:
                cart[str(product.id)]['product'] = product

            for item in cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        if self.user.is_authenticated:
            return sum(item.quantity for item in self.cart.items.all())
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.user.is_authenticated:
            return self.cart.get_total_price()
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        if self.user.is_authenticated:
            self.cart.items.all().delete()
        elif settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()