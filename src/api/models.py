from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=20)
    img = models.FileField(blank=True)
    desc = models.TextField(max_length=100)
    price = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=10)
    category = models.CharField(
        max_length=20,
        default='others',
        choices=
        (   
            ("electronics","Electronics"),
            ("clothing","clothing"),
            ("grocery","Grocery"),
            ("others","Others")
        )
    )
    def __str__(self):
        return self.name

class Wishlist(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_id.name

class Order(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.UUIDField(auto_created=True,blank=True)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    order_amount = models.IntegerField(blank=True,default=1)
    payment_status = models.BooleanField()

    def __str__(self):
        return str(self.order_id)