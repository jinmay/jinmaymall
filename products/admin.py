from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Product, Like, ProductImage
from .forms import ProductImageInlineFormset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', )

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    formset = ProductImageInlineFormset
    extra = 3

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    readonly_fields = ("hit", )
    list_display = ('name', 'price', 'is_active', )
    summernote_fields = ('long_desc', )
    inlines = [ProductImageInline]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass