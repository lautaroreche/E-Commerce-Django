from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=30)
    stock = models.IntegerField()
