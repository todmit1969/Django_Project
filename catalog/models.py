from django.db import models
from django.db.models import CASCADE


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Категория')
    category_desc = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return  f'{self.category_name}, {self.category_desc}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['category_name']


class Product(models.Model):
    product_name = models.CharField(max_length=50,verbose_name='Наименование')
    product_desc = models.CharField(max_length=150, verbose_name='Описание')
    product_image = models.ImageField(upload_to='catalog/images', blank=True, null=True)
    product_price = models.FloatField(verbose_name='Цена')
    created_at = models.DateField(verbose_name='Дата создания')
    updated_at = models.DateField(verbose_name='Дата изменения')
    product_category = models.ForeignKey(Category, on_delete=CASCADE, related_name='product')

    def __str__(self):
        return f'{self.product_name}, {self.product_price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['product_name']
