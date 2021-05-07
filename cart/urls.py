from django.urls import path, include
from . import views

app_name = 'cart'

urlpatterns = [
    path('<int:user_id>/',views.detail,name='detail'),
    path('add/<str:code>/',views.cart_add,name='cart_add'),
    path('remove/<str:code>/',views.cart_remove,name='cart_remove'),
]