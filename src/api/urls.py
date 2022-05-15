from .import views
from django.urls import path,include


urlpatterns = [
    path('fetch_all_products/', views.fetch_all_products,name='get'),
    path('add', views.add,name='add'),
    path('get_orders/', views.get_orders,name='get_orders'),
    path('fetch_wishlist/', views.fetch_wishlist,name='fetch_wishlist')
]
