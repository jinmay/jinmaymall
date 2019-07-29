from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.forms import CartForm
from .models import Category, Product, Like


UserModel = get_user_model()


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_total_count'] = Product.objects.filter(is_active=True).count()
        context['q'] = self.request.GET.get('q', "")
        context['qq'] = self.request.GET.get('qq', "")
        context['category_id'] = self.request.GET.get('category', None)
        return context

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        qq = self.request.GET.get('qq', None)
        category_id = self.request.GET.get('category', None)
        qs = Product.objects.filter_by_category(category_id)
        if q:
            qs = qs.filter(name__icontains=q)
        elif qq:
            qs = qs.filter(name__icontains=qq, category_id=category_id)
        return qs

product_list = ProductListView.as_view()


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    category_list = Category.objects.all()
    product_total_count = Product.objects.count()
    cart_form = CartForm()
    try:
        like = product.get_like(request.user)
    except:
        like = None

    return render(request, 'products/product_detail.html', {
        'cart_form': cart_form,
        'product': product,
        'category_list': category_list,
        'product_total_count': product_total_count,
        'like': like,
    })

# 유저 객체가 AnonymousUser클래스의 인스턴스인지 확인 후
# AnonymousUser의 객체 -> 로그인 페이지로 redirect
# 로그인한 유저 객체 -> 비동기로 좋아요 기능을 수행
@api_view(['POST'])
def toggle_like(request, product_id):
    user = request.user
    if isinstance(user, AnonymousUser):
        data = {
            'is_login': False
        }
        return Response(data=data, status=status.HTTP_200_OK)

    product = get_object_or_404(Product, pk=product_id)
    data = {
        'is_login': True,
        'is_existed': None
    }
    try:
        product_like = Like.objects.get(user=user, product=product)
        product_like.delete()
        data['is_existed'] = False
    except Like.DoesNotExist:
        Like.objects.create(user=user, product=product)
        data['is_existed'] = True
    
    return Response(data=data, status=status.HTTP_200_OK)


def like_list(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'products/wishlist.html', context)