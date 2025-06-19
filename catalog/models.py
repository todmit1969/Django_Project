from django.db import models
from django.db.models import CASCADE


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    desc = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return  f'{self.name}, {self.desc}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=50,verbose_name='Наименование')
    desc = models.TextField(max_length=150, verbose_name='Описание')
    image = models.ImageField(upload_to='catalog/images', blank=True, null=True)
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name='products')

    def __str__(self):
        return f'{self.name}, {self.price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
