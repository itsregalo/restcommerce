from django.db.models import fields
from rest_framework import serializers
from core.models import (Product, Category, ProductMedia,
                            OrderItem, CustomerOrder)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product

class ProductCreateSerializer(serializers.ModelField):
    class Meta:
        exclude = 'added_by'
        model = Product

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = ProductMedia


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = OrderItem

class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CustomerOrder