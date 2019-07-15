from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.product_set.count()

class ProductManager(models.Manager):
    def filter_by_category(self, category_id):
        if category_id:
            qs = Product.objects.filter(category_id=category_id)
        else:
            qs = Product.objects.all()
        return qs

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    price = models.IntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    hit = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'product_id': self.id})

    @property
    def like_count(self):
        return self.like.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user, self.product)