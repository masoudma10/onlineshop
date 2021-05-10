from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,SubCategory,Comment
from cart.forms import CartAddForm
from .forms import AddCommentForm,AddReplyForm,SearchProductForm
from django.contrib import messages


def home(request,slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if slug:
        category = get_object_or_404(Category,slug=slug)
        products = products.filter(sub_category__category=category)
    return render(request,'shop/home.html',{'products':products,'categories':categories})


def product_detail(request, slug):
    product = get_object_or_404(Product,slug=slug)
    comments = Comment.objects.filter(product=product, is_reply=False)
    form = CartAddForm()
    reply_form = AddReplyForm()
    if request.method == 'POST':
        form2 = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
            messages.success(request,'your comment submitted successfully','success')
    else:
        form2 = AddCommentForm()
    return render(request,'shop/product_detail.html', {'product':product,'form':form,
                                                       'comments':comments,'form2':form2,'reply':reply_form})



def sub_category(request, slug):
    subcategory = get_object_or_404(SubCategory,slug=slug)
    return render(request,'shop/sub_category.html',{'subcategories':subcategory})

@login_required
def add_reply(request,code,comment_id):
    product = get_object_or_404(Product,pk=code)
    comment = get_object_or_404(Comment,pk=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request,'your reply submitted','success')
    return redirect('shop:product_detail',product.slug)



































