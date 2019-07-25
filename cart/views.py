from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from .forms import CartForm


def cart_add(request, product_id):
    print('cart_add')
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    form = CartForm(request.POST)
    if form.is_valid():
        cd_quantity = form.cleaned_data['quantity']
        cd_update = form.cleaned_data['update']
        cart.add(product=product, quantity=cd_quantity, update=cd_update)
        return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    print('cart_remove')
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    print(cart.cart)
    return render(request, 'cart/cart.html')