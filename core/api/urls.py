from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ProductList, ProductDetail, CategoryList

urlpatterns = [
    path('product/', ProductList, name='product-list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', ProductDetail.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDetail.as_view(), name='product-delete'),
    path('product/create/', ProductDetail.as_view(), name='product-create'),

    path('category/', CategoryList.as_view(), name='category-list'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)