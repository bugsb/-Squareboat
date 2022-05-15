from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)