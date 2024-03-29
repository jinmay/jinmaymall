from django.core.validators import MaxValueValidator, MinValueValidator
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
        return self.product_set.filter(is_active=True).count()

class ProductManager(models.Manager):
    def filter_by_category(self, category_id):
        if category_id:
            qs = Product.objects.filter(category_id=category_id, is_active=True)
        else:
            qs = Product.objects.filter(is_active=True)
        return qs

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()
    is_representative = models.BooleanField()

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    price = models.IntegerField()
    short_desc = models.TextField()
    long_desc = models.TextField()
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

    @property
    def get_image(self):
        image = ProductImage.objects.get(product=self, is_representative=True)
        return image 

    def get_like(self, user):
        try:
            like = Like.objects.get(user=user, product=self)
        except Like.DoesNotExist:
            like = None
        return like

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user, self.product)


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-id', )

    def __str__(self):
        return self.title


class Answer(models.Model):
    qna = models.OneToOneField(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}의 답변".format(self.qna_id)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} 상품의 리뷰".format(self.product)