from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

app_name = 'api-core'

urlpatterns = [
    path('products/', ProductList, name='product-list'),
    path('product/<int:pk>/', ProductDetail, name='product-detail'),
    path('product/<int:pk>/update/', ProductUpdate, name='product-update'),
    path('product/<int:pk>/delete/', ProductDelete, name='product-delete'),
    path('product/create/', ProductCreate, name='product-create'),
    path('product/add-to-cart/<slug:slug>/', AddToCart, name='add-to-cart'),
    path('product/remove-fromm-cart/<slug:slug>/', RemoveFromCart, name='remove-fromm-cart'),

    path('category/', CategoryList, name='category-list'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)