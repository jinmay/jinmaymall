from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from products import views as products_views

def index(request):
    return redirect('products:product_list')

urlpatterns = [
    path('', index, name='root'),
    path('summernote/', include('django_summernote.urls')),

    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout, name='logout'),
    path('mypage/', accounts_views.mypage, name='mypage'),
    path('wishlist/', products_views.like_list, name='wishlist'),

    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)