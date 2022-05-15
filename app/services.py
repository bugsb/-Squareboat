from django.contrib.auth.models import User
from api.models import Product, Order, Wishlist, Cart

class Services:
    
    @staticmethod
    def remove_from_wishlist(added_by,product_id):
        wishlist = Wishlist.objects.select_related('added_by').get(
                added_by__username=added_by, product_id__id=product_id)
        wishlist.delete()

    @staticmethod
    def add_product_to_cart(user,product_id):
        product = Product.objects.get(id=product_id)
        user_id = User.objects.get(username=user)
        cart = Cart.objects.create(added_by=user_id, product_id=product)
        cart.save()
        
    @staticmethod
    def add_order(user_id,order_amount,product_id,payment_status):
        product = Product.objects.get(id=product_id)
        order = Order.objects.create(product_id=product,order_amount=1,ordered_by=user_id,payment_status=True)
        order.save()
    
    @staticmethod
    def add_item_to_wishlist(user,product_id):
        product = Product.objects.get(pk=product_id)
        user = User.objects.get(username=user)
        wishlist = Wishlist.objects.create(added_by=user, product_id=product)
        wishlist.save()

    @staticmethod
    def get_cart_items_for_user(user):
        cart_items = Cart.objects.select_related(
            'added_by').filter(added_by__username=user)
        return cart_items
    
    @staticmethod
    def get_all_products():
        products = Product.objects.all()
        return products
    
    @staticmethod
    def remove_from_cart(user,product_id):
        try:
            Cart.objects.select_related('added_by').get(
                added_by__username=user, product_id__id=product_id)
            cart.delete()
        except:
            pass

    @staticmethod
    def get_orders_for_user(user):
        orders = Order.objects.select_related(
        'ordered_by').filter(ordered_by__username=user)
        return orders
    
    @staticmethod
    def get_wishlist_for_user(user):
        wishlists = Wishlist.objects.select_related(
        'added_by').filter(added_by__username=user)
        return wishlists
    
    @staticmethod
    def get_user_object(user):
        user_object = User.objects.get(username=user)
        return user_object

    @staticmethod
    def get_cart_object(product_id):
        cart_object = Cart.objects.get(product_id=product_id)
        return cart_object
    
  