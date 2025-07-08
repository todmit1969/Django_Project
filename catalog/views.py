from django.shortcuts import render

def home(request):
    return render(request,'home.html')

def contacts(request):
    return render(request, 'contacts.html')

def products_list(request):
    return  render(request, 'products_list.html')