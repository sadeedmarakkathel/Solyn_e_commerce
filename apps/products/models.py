from django.db import models
from django.urls import reverse
from apps.category.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)
    inventory = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def get_absolute_url(self):
        return reverse('products:product_details', args=[self.id, self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'