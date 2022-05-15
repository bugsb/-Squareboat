from django.contrib import admin
from .models import Product,Order,Wishlist,Cart

admin.site.register((Product,Cart,Order,Wishlist))