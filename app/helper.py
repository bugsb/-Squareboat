from api.models import Wishlist, Cart

def is_item_in_cart(user,product_id):
    cart_items = Cart.objects.select_related('added_by').filter(
        added_by__username=user, product_id__id=product_id)

    if cart_items.first() is None:
        return False
    else:
        return True

def is_item_in_wishlist(user,product_id):
    items = Wishlist.objects.select_related('added_by').filter(
        added_by__username=user, product_id__id=product_id)
    
    if items.first() is None:
        return False
    else:
        return True