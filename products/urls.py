from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/likes/', views.toggle_like, name='toggle_like'),
    path('answer/<int:qna_id>/', views.answer, name='answer'),
]