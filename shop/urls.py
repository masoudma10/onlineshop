from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [
    path('',views.home,name='home'),
    path('category/<slug:slug>/', views.home, name='category'),
    path('sub_category/<slug:slug>/', views.sub_category, name='sub_category'),
    # path('category_detail/<slug:slug>/', views.category, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('search/product/<slug:slug>/', views.search_product, name='search_product'),
    path('add_reply/<str:code>/<int:comment_id>/', views.add_reply, name='add_reply'),

]