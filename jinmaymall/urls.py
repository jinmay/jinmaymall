from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include

def index(request):
    return redirect('products:product_list')

urlpatterns = [
    path('', index, name='root'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
]
