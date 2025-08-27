from django.core.management.base import BaseCommand
from unicodedata import category

from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'delete and add new categories and  products to the database'

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        category, _ = Category.objects.get_or_create(name = "Молочные продукты", desc = "Продукты произведенные из молока")

        products = [
            {'name': 'Молоко', 'price': '133', 'created_at' : '2025-06-16',
            'updated_at' : '2025-06-16', 'category':category},
        {'name': 'Брынза', 'price': '133', 'created_at' : '2025-06-16',
            'updated_at' : '2025-06-16', 'category':category}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Product: {product.name} added succefully'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Product: {product.name} already exist'))