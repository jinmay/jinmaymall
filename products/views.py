from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

product_list = ProductListView.as_view()