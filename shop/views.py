from django.shortcuts import render,get_object_or_404
from .models import Category,Product



def home(request):
    products = Product.objects.filter(available=True)
    return render(request,'shop/home.html',{'products':products})


def product_detail(request, slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'shop/product_detail.html', {'product':product})

