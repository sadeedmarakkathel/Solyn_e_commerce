from decimal import Decimal
from apps.products.models import Product
from django.shortcuts import get_object_or_404

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        flag=False
        if product.inventory==0:
            flag=True
            return flag

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "name": product.name,
                "image": product.image.url if product.image else ""
            }

        self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item


    def remove(self, id):
        product=get_object_or_404(Product,id=id)
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity']-=1
            if self.cart[product_id]['quantity']<=0:
                del self.cart[product_id]
        self.save()

    def remove_all(self, id):
        product=get_object_or_404(Product,id=id)
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def get_total_price(self):
        return sum(
            
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def __len__(self):
        return sum(id["quantity"] for id in self.cart.values())
    