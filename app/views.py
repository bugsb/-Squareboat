import json
from .helper import *
from .services import Services
from django.db.models import Sum
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse


def home(request):
    product = Services.get_all_products()
    context = {
        'data': product
    }
    return render(request, 'home.html', context=context)

def search(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        products = Services.search_product(key)
        context = {
            'data':products
        }
        return render(request, 'home.html', context=context)

@login_required(login_url='login')
def orders(request):
    user = request.user.username
    orders = Services.get_orders_for_user(user)
    context = {
        'data': orders
    }
    return render(request, 'orders.html', context=context)

@login_required(login_url='login')
def wishlists(request):
    user = request.user.username
    wishlists = Services.get_wishlist_for_user(user)
    context = {
        'data': wishlists,
        'page': 'wishlist'
    }
    return render(request, 'cart.html', context=context)


@csrf_exempt
def checkout(request):
    if request.body:
        data = json.loads(request.body)['data']  # json data from Js method

        user = request.user.username
        user_object = Services.get_user_object(user)
        for product_id in data:
            order = Services.add_order(user_id=user_object, order_amount=1,
                               product_id=product_id, payment_status=True)
            cart = Services.get_cart_object(product_id)
            cart.delete()
            print(order.order_id)
            messages.warning(request, message=f"Order Placed Successfully with order id {order.order_id} ")
        return HttpResponse({'message': "Checkout Success"})

@login_required(login_url='login')
def cart(request):
    user = request.user.username
    cart_items = Services.get_cart_items_for_user(user)
    total_items = cart_items.count()
    total_price = cart_items.aggregate(Sum('product_id__price'))[
        'product_id__price__sum']

    context = {
        'data': cart_items,
        'page': 'cart',
        'items': total_items,
        'price': total_price
    }
    return render(request, 'cart.html', context=context)

@login_required(login_url='login')
def remove_wishlist(request, product_id):
    user = request.user.username
    Services.remove_from_wishlist(added_by=user, product_id=product_id)
    messages.success(request, 'Item Removed from wishlist.')
    return redirect('wishlists')


@login_required(login_url='login')
def remove_cart(request, product_id):
    user = request.user.username
    Services.remove_from_cart(user, product_id)
    messages.success(request, 'Item Removed from cart.')
    return redirect('cart')

@login_required(login_url='login')
def add_to_cart(request, product_id):
    user = request.user.username

    if not is_item_in_cart(user, product_id):
        Services.add_product_to_cart(user=user, product_id=product_id)

        try:  # delete from wish list if exist
            Services.remove_from_wishlist(added_by=user, product_id=product_id)

        except:
            pass
        messages.success(request, 'Added to cart.')
    else:
        messages.success(request, 'Item already in the cart.')

    return redirect('home')

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    user = request.user.username
    
    if is_item_in_wishlist(user, product_id):
        Services.add_item_to_wishlist(user=user, product_id=product_id)
        messages.success(request, 'Added to Wishlist.')
    else:
        messages.success(request, 'Item already added to Wishlist.')

    return redirect('home')
