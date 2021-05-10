from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from shop.models import Product
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from accounts.models import User
from django.contrib import messages

@login_required
def detail(request,user_id):
    user = get_object_or_404(User,pk=user_id)
    if request.user.profile.address is None and request.user.profile.home_phone is None and request.user.profile.code_post is None :
        messages.error(request,'You must complete your profile','danger')
        return redirect('accounts:edit_profile',user.id )
    cart = Cart(request)
    return render(request,'cart/detail.html',{'cart':cart})


@require_POST
def cart_add(request,code):
    cart = Cart(request)
    product = get_object_or_404(Product,code=code)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'])

    return redirect('cart:detail',request.user.pk)

def cart_remove(request,code):
    cart = Cart(request)
    product = get_object_or_404(Product,code=code)
    cart.remove(product)
    return redirect('cart:detail',request.user.pk)
