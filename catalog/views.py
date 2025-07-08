from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ProductForm
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required, login_required
from .services import get_products_by_category


class HomeView(TemplateView):
    template_name = "home.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "one_product.html"
    context_object_name = "product"


def products_in_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = get_products_by_category(category_id)
    return render(
        request, "category_products.html", {"category": category, "products": products}
    )


def category_products(request, category_id):
    cache_key = f"category_{category_id}_products"
    products = cache.get(cache_key)

    if not products:
        products = list(get_products_by_category(category_id))
        cache.set(cache_key, products, timeout=60 * 10)

    category = get_object_or_404(Category, id=category_id)
    return render(
        request, "category_products.html", {"products": products, "category": category}
    )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["name", "description", "price", "is_published"]
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "object_list"


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ["name", "description", "price", "is_published"]
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.has_perm(
            "catalog.change_product"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.has_perm(
            "catalog.delete_product"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs["pk"])
        if product.is_published:
            product.is_published = False
            product.save()
        return redirect("catalog:product_list")


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "create_product.html", {"form": form})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.owner != request.user and not request.user.has_perm(
        "catalog.delete_product"
    ):
        raise PermissionDenied
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "edit_product.html", {"form": form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.owner != request.user and not request.user.has_perm(
        "catalog.delete_product"
    ):
        raise PermissionDenied
    product.delete()
    return redirect("catalog:product_list")