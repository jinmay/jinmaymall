from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from .models import Product, Like


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

product_list = ProductListView.as_view()


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product,
    })

@login_required
def toggle_like(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    try:
        product_like = Like.objects.get(user=user, product=product)
        product_like.delete()
    except Like.DoesNotExist:
        Like.objects.create(user=user, product=product)
    
    return redirect(product)