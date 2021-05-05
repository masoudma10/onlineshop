from django.shortcuts import render,get_object_or_404
from .models import Category,Product,SubCategory



def home(request,slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if slug:
        category = get_object_or_404(Category,slug=slug)
        products = products.filter(sub_category__category=category)
    return render(request,'shop/home.html',{'products':products,'categories':categories})


def product_detail(request, slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'shop/product_detail.html', {'product':product})



def sub_category(request, slug):
    subcategory = get_object_or_404(SubCategory,slug=slug)
    return render(request,'shop/sub_category.html',{'subcategories':subcategory})
