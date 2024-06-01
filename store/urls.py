from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.store, name='store'),
    path('<str:slug>/', views.productDetail, name='product-detail'),
]
