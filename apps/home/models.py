from django.db import models

# Create your models here.
# apps/home/models.py
class Hero(models.Model):
    headline = models.CharField(max_length=200)
    subtext = models.TextField()
    image = models.ImageField(upload_to='hero/')
    primary_cta_text = models.CharField(max_length=50)
    primary_cta_link = models.CharField(max_length=200)
    secondary_cta_text = models.CharField(max_length=50, blank=True)
    secondary_cta_link = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.headline
