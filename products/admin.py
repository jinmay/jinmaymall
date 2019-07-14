from django.contrib import admin
from .models import Category, Product, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("hit", )
    list_display = ('name', 'price', 'is_active', )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass