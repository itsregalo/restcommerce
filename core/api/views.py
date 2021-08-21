from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime

from core.models import (Category, Product, ProductMedia, 
                            OrderItem,CustomerOrder)
from .serializers import (
                    CategorySerializer,
                    CustomerOrderSerializer,
                    ProductCreateSerializer,
                    ProductSerializer,
                    ProductMediaSerializer,
                    CustomerOrderSerializer,
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

    product = Product(added_by_merchant = request.user.merchantuser)
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

    if owner != product.added_by_merchant.user:
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
def AddToCart(request, pk):
    product = Product.objects.get(pk=pk)

    order_item, created = OrderItem.objects.get_or_create(user=request.user,
                                                          product=product,
                                                          is_ordered=False)
    order_qs = CustomerOrder.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity has been updated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            order.products.add(order_item)
            messages.info(request, "product has been added to the cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        order = CustomerOrder.objects.create(user=request.user)
        order.products.add(order_item)
        messages.info(request, "Item has been added")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def CartListView(request):
    try:
        customer_order = CustomerOrder.objects.get(user=request.user)
    except CustomerOrder.DoesNotExist:
        return Response({'response':'You do not have any item in Your cart'})

    serializer = CustomerOrderSerializer(customer_order)
    return Response(serializer.data)
