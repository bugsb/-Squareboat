from django.contrib import admin
from .models import Product,Order,Wishlist,Cart
# Register your models here.
admin.site.register((Product,Cart,Order,Wishlist))