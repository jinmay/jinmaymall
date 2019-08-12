from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.forms import CartForm
from .models import Category, Product, Like, Post, Review
from .forms import QnaForm, AnswerForm, ReviewForm, ReviewEditForm


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
    qna_list = Post.objects.filter(product=product)
    cart_form = CartForm()
    qnaform = QnaForm()
    review_form = ReviewForm()
    try:
        like = product.get_like(request.user)
    except:
        like = None

    if request.user.is_staff:
        answer_form = AnswerForm()
    else:
        answer_form = None

    if request.method == 'POST':
        form = QnaForm(request.POST)
        if form.is_valid():
            qna = form.save(commit=False)
            qna.author = request.user
            qna.product =product
            qna.save()
            return redirect(product)

    return render(request, 'products/product_detail.html', {
        'cart_form': cart_form,
        'product': product,
        'category_list': category_list,
        'product_total_count': product_total_count,
        'like': like,
        'qnaform': qnaform,
        'qna_list': qna_list,
        'answer_form': answer_form,
        'review_form': review_form,
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


# 위시리스트
def like_list(request):
    return render(request, 'products/wishlist.html')

# QnA의 답변을 생성하는 함수입니다
def answer(request, qna_id):
    qna = get_object_or_404(Post, pk=qna_id)
    product = qna.product
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.qna = qna
            answer.save()
            return redirect(product)

# 새로운 리뷰 생성에 사용할 함수입니다
def review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    # 이미 작성한 리뷰가 있으면 리뷰를 생성하는 로직을 거치지 않고
    # 현재의 상품으로 리다이렉트 합니다
    review = Review.objects.filter(product=product, user=user)
    if review:
        return redirect(product)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = user
            review.save()
            return redirect(product)
        return redirect(product)

# 리뷰 게시글 수정에 사용할 함수입니다
def review_edit(request, product_id, review_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(Review, pk=review_id)

    if request.method == 'POST':
        form = ReviewEditForm(request.POST, instance=review)
        print(form)
        if form.is_valid():
            print('valid')
            edited_review = form.save(commit=False)
            edited_review.title = review.title
            edited_review.product = product
            edited_review.user = user
            edited_review.rating = review.rating
            edited_review.save()
            return redirect(product)
        print('invalid')
        return redirect(product)

# 리뷰 게시글 삭제 함수
@api_view(['GET'])
def review_delete(request, product_id, review_id):
    if request.is_ajax():
        review = get_object_or_404(Review, pk=review_id, product_id=product_id, user=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)