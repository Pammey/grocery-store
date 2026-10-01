from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Vegetables"
        )

        self.product = Product.objects.create(
            name="Fresh Broccoli",
            description="Fresh green broccoli",
            price=1500.00,
            sale_price=1200.00,
            stock=10,
            category=self.category,
        )

    def test_product_slug_is_generated(self):
        self.assertEqual(self.product.slug, "fresh-broccoli")

    def test_product_is_on_sale(self):
        self.assertTrue(self.product.is_on_sale)

    def test_display_price_returns_sale_price(self):
        self.assertEqual(self.product.get_display_price, self.product.sale_price)

    def test_product_absolute_url(self):
        expected_url = reverse(
            "product_detail",
            args=[self.product.slug]
        )
        self.assertEqual(self.product.get_absolute_url(), expected_url)


class ProductDetailViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Fruits"
        )

        self.product = Product.objects.create(
            name="Fresh Mango",
            description="Sweet fresh mangoes",
            price=2000.00,
            stock=5,
            category=self.category,
        )

    def test_product_detail_page_loads(self):
        response = self.client.get(
            reverse("product_detail", args=[self.product.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_returns_404_for_invalid_slug(self):
        response = self.client.get(
            reverse("product_detail", args=["does-not-exist"])
        )

        self.assertEqual(response.status_code, 404)