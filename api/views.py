from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from api.models import Product,Order,Wishlist
from rest_framework.decorators import api_view
from .serializers import ProductSerializer,OrderSerializer,WishlistSerializer


@api_view(['GET'])
def fetch_all_products(request):
    items = Product.objects.all()
    serializer = ProductSerializer(items,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=400,data=serializer.errors)

@api_view(['GET'])
def get_orders(request):
    try:
        user_id = request.GET['user']
    except KeyError:
        return Response(status=400,data={"Invalid query parameters"})
    print(user_id)
    orders = Order.objects.select_related('ordered_by').filter(ordered_by__username=user_id)
    serializer = OrderSerializer(orders,many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def fetch_wishlist(request):
    try:
        user_id = request.GET['user']
    except KeyError:
        return Response(status=400,data={"Invalid query parameters"})
    print(user_id)
    orders = Wishlist.objects.select_related('added_by').filter(added_by__username=user_id)
    serializer = WishlistSerializer(orders,many=True)
    return Response(data=serializer.data)