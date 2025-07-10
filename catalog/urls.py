from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, single_product

app_name = CatalogConfig.name

urlpatterns = [
    path('',home, name='home'),
    path('contacts/',contacts, name='contacts'),
    path("product/<int:pk>/", single_product, name="single_product")
]