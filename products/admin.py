from django.contrib import admin
from .models import Category, Product, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["hit"]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass