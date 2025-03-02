from django.db import models
from cloudinary.models import CloudinaryField


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    image = CloudinaryField('image', resource_type='image')
    category = models.CharField(max_length=30)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.id} > {self.name}"


class Payment(models.Model):
    method = models.CharField(
        max_length=20,
        choices=[
            ('Credit Card', 'Credit Card'),
            ('Debit Card', 'Debit Card'),
            ('Bank Transfer', 'Bank Transfer'),
            ('Cash', 'Cash'),
            ('Other', 'Other'),
        ],
        default='Credit Card'
    )
    detail = models.CharField(max_length=100, default='')
    token = models.CharField(max_length=255, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Failed', 'Failed'),
            ('Refunded', 'Refunded'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"{self.id}"


class Order(models.Model):
    products = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class SuscriptorNewsletter(models.Model):
    email = models.EmailField(unique=True, max_length=100)

    def __str__(self):
        return f"{self.id} > {self.email}"
