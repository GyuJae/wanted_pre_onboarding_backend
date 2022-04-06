from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import (
    ProductSerializer,
    CreateProductSerializer,
    UpdateProductSerializer,
)
from .models import Product
from products import serializers


class ProductList(APIView):

    """List all products, or creat e a new product"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(sef, request, format=None):
        if request.query_params.get("search"):
            keyword = request.query_params.get("search")
            products = Product.objects.filter(title__contains=keyword)
        elif request.query_params.get("order_by"):
            order_keyword = request.query_params.get("order_by")
            if order_keyword == "생성일":
                products = Product.objects.all().order_by("-created_at")
            elif order_keyword == "총펀딩금액":
                products = Product.objects.all().order_by("-total_amount")
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        data["publisher"] = request.user.id
        print(request.user.id)
        serializer = CreateProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(publisher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):

    """
    Retrieve, update or delete a code product.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        product = self.get_object(pk)
        if product.publisher_name() != request.user.username:
            return Response(
                {"details": "not your product"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UpdateProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductFunding(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        product.participants.add(request.user)
        product.total_amount += product.one_time_funding_amount
        product.save()
        return Response(status=status.HTTP_200_OK)
