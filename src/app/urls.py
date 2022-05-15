from django.urls import path,include
from .import views
urlpatterns = [
    path('', views.home,name='home'),
    path('orders/', views.orders,name='orders'),
    path('wishlists/', views.wishlists,name='wishlists'),
    path('cart/', views.cart,name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart,name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>', views.add_to_wishlist,name='add_to_wishlist'),
    path('checkout/', views.checkout,name='checkout'),
    path('remove_wishlist/<int:product_id>', views.remove_wishlist,name='remove_wishlist'),
    path('remove_cart/<int:product_id>', views.remove_cart,name='remove_cart'),
]
