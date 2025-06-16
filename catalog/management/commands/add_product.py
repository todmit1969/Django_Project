from django.core.management.base import BaseCommand
from unicodedata import category

from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'delete and add new categories and  products to the database'

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        category, _ = Category.objects.get_or_create(category_name = "Молочные продукты", category_desc = "Продукты произведенные из молока")

        products = [
            {'product_name': 'Молоко', 'product_price': '133', 'created_at' : '2025-06-16',
            'updated_at' : '2025-06-16', 'product_category':category},
        {'product_name': 'Брынза', 'product_price': '133', 'created_at' : '2025-06-16',
            'updated_at' : '2025-06-16', 'product_category':category}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Product: {product.product_name} added succefully'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Product: {product.product_name} already exist'))