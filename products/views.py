from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Like


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_total_count'] = Product.objects.count()
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        qs = Product.objects.filter_by_category(category_id)
        return qs

product_list = ProductListView.as_view()


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    category_list = Category.objects.all()
    product_total_count = Product.objects.count()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'category_list': category_list,
        'product_total_count': product_total_count,
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