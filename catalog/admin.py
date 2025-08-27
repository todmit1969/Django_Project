from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =('id', 'name',)
    search_fields = ('name', 'desc',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category','image')
    list_filter = ('category',)
    search_fields = ('name', 'desc',)

