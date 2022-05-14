from django.shortcuts import render
from api.models import Product
# Create your views here.
def home(request):
    product = Product.objects.all()
    context = {
        'data':product
    }
    return render(request,'home.html',context=context)