# scraper/models.py
from django.db import models

class SKU(models.Model):
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.color} - {self.size}"
    
    class Meta:
        app_label = 'scraper'

class Product(models.Model):
    category = models.CharField(max_length=255, default="Uncategorized")

    url = models.URLField(unique=True, default="Unknown")
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    MRP = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    img=models.URLField(blank=True , null=True)
    last_7_day_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fit = models.CharField(max_length=100, default="Unknown")
    fabric = models.CharField(max_length=100, default="Unknown")
    neck = models.CharField(max_length=100, default="Unknown")
    sleeve = models.CharField(max_length=100, default="Unknown")
    pattern = models.CharField(max_length=100, default="Unknown")
    length = models.CharField(max_length=100 ,default="Unknown")
    description = models.TextField()
    available_skus = models.ManyToManyField(SKU, related_name='products')

    def __str__(self):
        return self.title
    
    
    class Meta:
        app_label = 'scraper'
