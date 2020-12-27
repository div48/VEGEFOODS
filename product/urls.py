from django.conf.urls import url
from . import views
from django.urls import path, include




urlpatterns = [



    path('',views.index,name="index" ),
    path('cart', views.cart, name="cart"),
    path('about', views.about, name="about"),
    path('home', views.home, name="home"),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('order-summary/', views. order_details, name='order-summary'),
    path('delete-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('checkout', views.checkout, name="checkout"),
    path('add', views.add, name='add'),
path('sucess', views.sucess, name='sucess'),
    # path('place_order', views.add, name="add"),




]
