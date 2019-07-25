from django.conf import settings
from products.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_KEY, None)
        if cart is None:
            cart = self.session[settings.CART_SESSION_KEY] = {}
        self.cart = cart

    def __iter__(self):
        product_id_list = self.cart.keys()
        product_list = Product.objects.filter(id__in=product_id_list)
        for product in product_list:
            self.cart[str(product.id)]['product'] = product
            # yield (product.id, self.cart[str(product.id)])

        for product in self.cart.values():
            product['total_price'] = product['price'] * product['quantity']
            yield product

    def add(self, product, quantity=1, update=False):
        print('add CART')
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = { 'quantity': 0, 'price': product.price }
        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def save(self):
        self.session[settings.CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        target_id = str(product_id)
        if target_id in self.cart:
            del self.cart[target_id]
            self.save()

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())