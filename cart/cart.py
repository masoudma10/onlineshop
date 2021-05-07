from shop.models import Product


CART_SESSION_ID = 'cart'


class Cart:

    def __init__(self,request):
        """
        this cons give session and save it
        :param request:
        """
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_codes = self.cart.keys()
        products = Product.objects.filter(code__in=product_codes)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.code)]['product'] = product

        for item in cart.values():

            item['total_price'] = int(item['price']) * item['quantity']
            yield item



    def add(self,product,quantity=1):
        product_code = str(product.code)


        if product_code not in self.cart:
            self.cart[product_code] = {'quantity':0,'price':str(product.price)}

        self.cart[product_code]['quantity'] += quantity
        self.save()


    def get_total_price(self):
        return sum(int(item['price'])*item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True


    def remove(self,product):
        product_code = str(product.code)
        if product_code in self.cart:
            del self.cart[product_code]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
