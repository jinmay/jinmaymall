from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product
from .cart import Cart
from .forms import CartForm


@api_view(['POST'])
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    form = CartForm(request.POST)
    if form.is_valid():
        is_detail = request.POST.get('is_detail', None)
        cd_quantity = form.cleaned_data['quantity']
        cd_update = form.cleaned_data['update']
        cart.add(product=product, quantity=cd_quantity, update=cd_update)
        if request.is_ajax():
            return Response(status=status.HTTP_201_CREATED)
        if is_detail is not None:
            return redirect(product)
        return redirect('cart:cart_detail')

@api_view(['GET'])
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    if request.is_ajax():
        data = {
            'get_total_price': cart.get_total_price(),
            'total_count': len(cart),
        }
        return Response(data=data)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for product in cart:
        product['update_quantity_form'] = CartForm(initial={'quantity': product['quantity'], 'update': True})
    return render(request, 'cart/cart.html')