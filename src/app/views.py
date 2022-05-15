from django.shortcuts import render, redirect, HttpResponse
from api.models import Product, Order, Wishlist, Cart
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import json
from django.contrib import messages
# Create your views here.


def home(request):
    product = Product.objects.all()
    context = {
        'data': product
    }
    return render(request, 'home.html', context=context)


def orders(request):
    user = request.GET['user']
    orders = Order.objects.select_related(
        'ordered_by').filter(ordered_by__username=user)
    context = {
        'data': orders
    }
    print(context)
    return render(request, 'orders.html', context=context)


def wishlists(request):
    user = request.user.username
    wishlists = Wishlist.objects.select_related(
        'added_by').filter(added_by__username=user)
    context = {
        'data': wishlists,
        'page': 'wishlist'
    }
    print(context)
    return render(request, 'cart.html', context=context)


@csrf_exempt
def checkout(requests):
    if requests.body:
        data = json.loads(requests.body)['data']
    
        print(data)
        user = requests.user.username
        user_id = User.objects.get(username=user)
        for product_id in data:
            product = Product.objects.get(id=product_id)
            order = Order.objects.create(product_id=product,order_amount=1,ordered_by=user_id,payment_status=True)
            order.save()
            print('order saved')
            cart = Cart.objects.get(product_id=product)
            cart.delete()
            print('deleted from cart')
        return HttpResponse({'data': "Checkout Success"})


def cart(request):
    user = request.user.username
    cart_items = Cart.objects.select_related(
        'added_by').filter(added_by__username=user)
    total_items = cart_items.count()
    total_price = cart_items.aggregate(Sum('product_id__price'))[
        'product_id__price__sum']
    print(total_price)
    context = {
        'data': cart_items,
        'page': 'cart',
        'items': total_items,
        'price': total_price
    }
    print(context)
    return render(request, 'cart.html', context=context)

def remove_wishlist(request,product_id):
    user = request.user.username
    wishlist = Wishlist.objects.select_related('added_by').get(
                added_by__username=user, product_id__id=product_id)
    print(wishlist)
    wishlist.delete()
    messages.success(request, 'Item Removed from wishlist.')
    return redirect('wishlists')

def remove_cart(request,product_id):
    user = request.user.username
    wishlist = Cart.objects.select_related('added_by').get(
                added_by__username=user, product_id__id=product_id)
    wishlist.delete()
    messages.success(request, 'Item Removed from cart.')
    return redirect('cart')

def add_to_cart(request, id):
    user = request.user.username
    cart_items = Cart.objects.select_related('added_by').filter(
        added_by__username=user, product_id__id=id)
    print(cart_items)
    if cart_items.first() is None:
        product = Product.objects.get(id=id)
        user_id = User.objects.get(username=user)
        cart = Cart.objects.create(added_by=user_id, product_id=product)
        cart.save()
        try:  # delete from wish list if exist
            wishlist = Wishlist.objects.select_related('added_by').get(
                added_by__username=user, product_id__id=id)
            print(wishlist)
            wishlist.delete()
            print('delete ho gya')
            
        except:
            print('Wl mei ni hai')
        messages.success(request, 'Added to cart.')        
    else:
        messages.success(request, 'Item already in the cart.')
    return redirect('home')


def add_to_wishlist(request, id):
    user = request.user.username
    items = Wishlist.objects.select_related('added_by').filter(
        added_by__username=user, product_id__id=id)
    print(items)
    if items.first() is None:
        product = Product.objects.get(id=id)
        user = User.objects.get(username=user)
        wishlist = Wishlist.objects.create(added_by=user, product_id=product)
        wishlist.save()
        messages.success(request, 'Added to Wishlist.')
    else:
        messages.success(request, 'Item not added to Wishlist.')

    return redirect('home')
