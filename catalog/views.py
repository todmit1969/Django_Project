from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProductForm
from .models import Product, Category
from .services import products_by_category

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = "home.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = "single_product.html"
    context_object_name = "product"

    def get_queryset(self):
        queryset = cache.get('category_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('category_queryset', queryset, 60 * 15)
        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_moderator = self.request.user.groups.filter(name="Модератор").exists()
        context["is_moderator"] = is_moderator
        return context

class ProductByCategoryListView(ListView):
    model = Product
    template_name = "product_by_category.html"

    def get_queryset(self):
        category_id = self.request.GET.get("category")

        return products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_moderator = self.request.user.groups.filter(
            name="Модератор продуктов"
        ).exists()

        context["is_moderator"] = is_moderator
        categories = Category.objects.all()
        context["categories"] = categories

        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        product = super().get_object()
        if product.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Вы не можете изменять этот продукт!")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        product = super().get_object()
        if product.owner == self.request.user or request.user.has_perm("catalog:delete_product"):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Вы не можете удалить этот продукт!")

class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет прав для снятия продукта с публикации!")
        product.is_published = False
        product.save()
        return redirect("catalog:products_list")
