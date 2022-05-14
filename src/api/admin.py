from django.contrib import admin
from .models import Product,Order,Wishlist
# Register your models here.
admin.site.register((Product,Order,Wishlist))