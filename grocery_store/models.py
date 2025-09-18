from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True,max_length=200)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    def is_on_sale(self):
        """A helper property to easily check if a product is on sale."""
        return self.sale_price is not None and self.sale_price < self.price

    @property
    def get_display_price(self):
        """A helper property to return the correct price to display in templates."""
        if self.is_on_sale:
            return self.sale_price
        return self.price  

