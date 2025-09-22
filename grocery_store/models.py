from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

def generate_unique_slug(instance, value_field='name', slug_field='slug'):
    """
    Generate a unique slug for `instance` based on `value_field`.
    Works by slugifying the value and appending a counter if needed.
    """
    base = slugify(getattr(instance, value_field))
    slug = base
    ModelClass = instance.__class__
    counter = 1

    # Build query for existing slugs (exclude current instance when updating)
    while True:
        lookup = {slug_field: slug}
        qs = ModelClass.objects.filter(**lookup)
        if instance.pk:
            qs = qs.exclude(pk=instance.pk)
        if not qs.exists():
            return slug
        slug = f"{base}-{counter}"
        counter += 1


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True,max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, value_field='name', slug_field='slug')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unit = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'kg', 'liters', 'pcs'


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, value_field='name', slug_field='slug')
        super().save(*args, **kwargs)


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

