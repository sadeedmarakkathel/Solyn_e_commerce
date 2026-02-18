from django.conf import settings
from django.db import models
from apps.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )
    
    PAYMENT_CHOICES = (
        ("card", "Credit/Debit Card"),
        ("paypal", "PayPal"),
        ("cod", "Cash on Delivery"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="card"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    shipping_status = models.CharField(
        max_length=50,
        default="Processing",
        choices=(
            ("Processing", "Processing"),
            ("Shipped", "Shipped"),
            ("In Transit", "In Transit"),
            ("Delivered", "Delivered"),
            ("Returned", "Returned"),
            ("Cancelled", "Cancelled")
        )
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
