from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import ( HomeView,
                            ContactsView,
                            ProductListView,
                            ProductCreateView,
                            ProductDetailView,
                            ProductUpdateView,
                            ProductDeleteView
                           )

app_name = CatalogConfig.name

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="single_product"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    )
]