from django.shortcuts import render
from catalog.models import Product

def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"object_list": products})

def contacts(request):
    return render(request, 'contacts.html')

def single_product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "single_product.html", {"product": product})