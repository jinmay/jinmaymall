from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

product_list = ProductListView.as_view()


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product,
    })