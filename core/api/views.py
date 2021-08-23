from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime

from core.models import (Category, Product, ProductMedia, 
                            OrderItem,CustomerOrder)
from .serializers import (
                    CategorySerializer,
                    CartSerializer,
                    OrderItemSerializer,
                    ProductCreateSerializer,
                    ProductSerializer,
                    ProductMediaSerializer,
                    
                    )

@api_view(['GET'])
def ProductList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def ProductDetail(request,  pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def ProductCreate(request):
    
    if request.user.is_merchant == False:
        return Response({'response':"You are not a merchant"})

    product = Product(added_by = request.user)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def ProductUpdate(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    owner = request.user

    if owner != product.added_by.user:
        return Response({'response':"You are not the owner of this product"})

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def ProductDelete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    print(product.added_by_merchant.user)

    owner = request.user
    if owner != product.added_by_merchant.user:
        return Response({'response':"You are not the owner of this product"})

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def CategoryList(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated))
def AddToCart(request, slug):
    product = Product.objects.get(slug=slug)

    order_item, created = OrderItem.objects.get_or_create(user=request.user,
                                                          product=product,
                                                          is_ordered=False)
    order_qs = CustomerOrder.objects.filter(user=request.user, is_ordered=False)
    data = {}
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            serializer = OrderItemSerializer(order_item)
            data['success'] = "Item was added to cart"
            data['item'] = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        order.products.add(order_item)
        serializer = OrderItemSerializer(order_item)
        data['success'] = "Item was added to cart"
        data['item'] = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    serializer = OrderItemSerializer(order_item)
    data['success'] = "Item was added to cart"
    data['product'] = serializer.data
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes((IsAuthenticated))
def RemoveFromCart(request, slug, *args, **kwargs):
    product = get_object_or_404(Product, slug=slug)
    order_qs = CustomerOrder.objects.filter(user=request.user)
    data = {}
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(user=request.user,
                                                  product=product,
                                                  is_ordered=False)[0]
            order.products.remove(order_item)
            serializer = OrderItemSerializer(product)
            data['success'] = 'Item removed from cart'
            data['product'] = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        data['failure'] = 'Item not cart'
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    data['failure'] = 'You do not have an active order'
    return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def CartListView(request):
    try:
        customer_order = CustomerOrder.objects.get(user=request.user)
    except CustomerOrder.DoesNotExist:
        return Response({'response':'You do not have any item in Your cart'})

    serializer = CartSerializer(customer_order, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def CategoryList(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
    except Category.DoesNotExist:
        return Response({'response':'You do not have any category yet'})
    products = Product.objects.filter(category=category)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
