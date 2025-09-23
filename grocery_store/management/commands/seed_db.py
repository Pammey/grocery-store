# your_app/management/commands/seed_db.py

import decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db import transaction

# IMPORTANT: Replace 'shop' with the actual name of your app containing the models
from grocery_store.models import Category, Product 

# Data for seeding the database
# =========================================================================
CATEGORIES = [
    "Grains, Tubers & Pantry",
    "Vegetables & Leafy Greens",
    "Fruits",
    "Meat & Poultry",
    "Fish & Seafood",
    "Soups & Stew Ingredients",
    "Dairy & Eggs",
    "Bakery & Confectionery",
    "Beverages",
    "Household & Cleaning",
]

PRODUCTS = [
    # Grains, Tubers & Pantry
    {'name': 'Tubers of Yam', 'description': 'Large, hearty tubers of yam, perfect for pounding, boiling, or frying. Sourced from the best farms.', 'price': decimal.Decimal('3500.00'), 'category_name': 'Grains, Tubers & Pantry', 'stock': 50},
    {'name': 'Ijebu Garri', 'description': 'Fine, sour cassava flakes with a distinctive taste. Ideal for making Eba.', 'price': decimal.Decimal('2500.00'), 'category_name': 'Grains, Tubers & Pantry', 'stock': 100},
    {'name': 'Ofada Rice', 'description': 'Authentic, locally grown brown rice with its signature aroma and flavour.', 'price': decimal.Decimal('4000.00'), 'category_name': 'Grains, Tubers & Pantry', 'stock': 80},
    {'name': 'Oloyin Beans', 'description': 'Premium "Honey Beans" known for their unique sweet taste. Cooks soft and is perfect for Ewa Aganyin.', 'price': decimal.Decimal('3800.00'), 'category_name': 'Grains, Tubers & Pantry', 'stock': 120},
    {'name': 'Kings Vegetable Oil', 'description': 'Cholesterol-free vegetable oil, perfect for all your cooking and frying needs.', 'price': decimal.Decimal('9500.00'), 'category_name': 'Grains, Tubers & Pantry', 'stock': 40},
    {'name': 'Knorr Seasoning Cubes', 'description': 'A pack of essential seasoning cubes for every Nigerian kitchen.', 'price': decimal.Decimal('1200.00'), 'category_name': 'Grains, Tubers & Pantry', 'stock': 200},
    
    # Vegetables & Leafy Greens
    {'name': 'Ripe Tomatoes', 'description': 'A basket of fresh, ripe red tomatoes, essential for stews, Jollof, and sauces.', 'price': decimal.Decimal('4500.00'), 'category_name': 'Vegetables & Leafy Greens', 'stock': 30},
    {'name': 'Atarodo (Scotch Bonnet)', 'description': 'A handful of fiery hot Scotch Bonnet peppers (Atarodo) to add that signature Nigerian heat.', 'price': decimal.Decimal('1000.00'), 'category_name': 'Vegetables & Leafy Greens', 'stock': 150},
    {'name': 'Ugu Leaves (Pumpkin)', 'description': 'Fresh pumpkin leaves, pre-washed and sliced for your convenience.', 'price': decimal.Decimal('800.00'), 'category_name': 'Vegetables & Leafy Greens', 'stock': 100},
    {'name': 'Red Onions', 'description': 'A bag of large, crisp red onions. A staple ingredient for flavouring almost any dish.', 'price': decimal.Decimal('2000.00'), 'category_name': 'Vegetables & Leafy Greens', 'stock': 90},
    
    # Fruits
    {'name': 'Sweet Pineapple', 'description': 'Juicy and sweet pineapple, freshly harvested. Enjoy it as a healthy snack.', 'price': decimal.Decimal('2500.00'), 'category_name': 'Fruits', 'stock': 60},
    {'name': 'Medium Watermelon', 'description': 'A refreshing, hydrating medium-sized watermelon. Perfect for hot afternoons.', 'price': decimal.Decimal('4000.00'), 'category_name': 'Fruits', 'stock': 25},
    {'name': 'Ripe Plantain', 'description': 'A bunch of sweet, ripe plantain, ready to be fried into delicious Dodo.', 'price': decimal.Decimal('1800.00'), 'category_name': 'Fruits', 'stock': 80},
    
    # Meat & Poultry
    {'name': 'Whole Chicken (Broiler)', 'description': 'A whole dressed chicken, cleaned and ready for roasting or cutting into pieces. Approx. 1.5kg.', 'price': decimal.Decimal('8500.00'), 'category_name': 'Meat & Poultry', 'stock': 35},
    {'name': 'Assorted Goat Meat', 'description': 'A mix of goat meat cuts, perfect for stews, peppersoup, and traditional dishes.', 'price': decimal.Decimal('6000.00'), 'category_name': 'Meat & Poultry', 'stock': 45},
    {'name': 'Beef for Stewing', 'description': 'Freshly cut beef with minimal fat, ideal for slow-cooking in your favourite Nigerian stews.', 'price': decimal.Decimal('5500.00'), 'category_name': 'Meat & Poultry', 'stock': 50},
    
    # Fish & Seafood
    {'name': 'Croaker Fish (Medium)', 'description': 'Fresh, whole croaker fish, scaled and gutted for your convenience.', 'price': decimal.Decimal('4500.00'), 'category_name': 'Fish & Seafood', 'stock': 40},
    {'name': 'Smoked Catfish (Eja Kika)', 'description': 'Dried and smoked catfish that adds a deep, smoky flavour to soups and stews.', 'price': decimal.Decimal('3000.00'), 'category_name': 'Fish & Seafood', 'stock': 100},
    {'name': 'Ground Crayfish', 'description': 'A bag of ground crayfish, ready to be sprinkled into your soups for an authentic taste.', 'price': decimal.Decimal('2500.00'), 'category_name': 'Fish & Seafood', 'stock': 120},
    
    # Soups & Stew Ingredients
    {'name': 'Egusi (Ground Melon Seeds)', 'description': 'Finely ground melon seeds, the primary ingredient for making delicious Egusi soup.', 'price': decimal.Decimal('3000.00'), 'category_name': 'Soups & Stew Ingredients', 'stock': 70},
    {'name': 'Ogbono (Ground)', 'description': 'Ground African Bush Mango seeds, ready to use for making rich and flavourful Ogbono soup.', 'price': decimal.Decimal('3500.00'), 'category_name': 'Soups & Stew Ingredients', 'stock': 65},
    {'name': 'Stockfish (Panla)', 'description': 'Dried and de-boned Panla (Cod) stockfish, cleaned and cut into pieces for easy use in soups.', 'price': decimal.Decimal('4000.00'), 'category_name': 'Soups & Stew Ingredients', 'stock': 55},
]
# =========================================================================


class Command(BaseCommand):
    help = 'Seeds the database with initial categories and products for FreshDirect.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding process...'))

        # --- Clear existing data to prevent duplicates ---
        self.stdout.write('Clearing old data...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old data cleared.'))

        # --- Create Categories ---
        self.stdout.write('Creating categories...')
        for category_name in CATEGORIES:
            Category.objects.create(
                name=category_name,
                slug=slugify(category_name)
            )
        self.stdout.write(self.style.SUCCESS('All categories created.'))

        # --- Create Products ---
        self.stdout.write('Creating products...')
        for product_data in PRODUCTS:
            try:
                # Find the category object by its name
                category_name = product_data.pop('category_name')
                category_obj = Category.objects.get(name=category_name)

                # Create the product
                Product.objects.create(
                    category=category_obj,
                    slug=slugify(product_data['name']),
                    **product_data # Pass the rest of the dict as kwargs
                )
                self.stdout.write(f"  - Added product: {product_data['name']}")

            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category '{category_name}' not found for product '{product_data['name']}'. Skipping."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred with product '{product_data['name']}': {e}"))
        
        self.stdout.write(self.style.SUCCESS('All products created.'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))