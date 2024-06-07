from django.urls import path 
from . import views


urlpatterns = [
    path('', views.cart, name='cart'), 
    path('add_cart/<str:pk>', views.add_cart, name='add-cart'),
    path('reduce/<str:pk>', views.reduce_quantity, name='reduce'),
    path('remove/<str:pk>', views.remove, name='remove'),
    path('checkout', views.checkout, name='checkout'), 
]
