from django.contrib import admin
from .models import Category, Product, Like, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', )

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("hit", )
    list_display = ('name', 'price', 'is_active', )
    inlines = [ProductImageInline]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass