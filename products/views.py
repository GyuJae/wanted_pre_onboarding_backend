from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    ProductSerializer,
    CreateProductSerializer,
    UpdateProductSerializer,
)
from .models import Product


@api_view(["GET", "POST"])
def product_list(request):

    """
    List all code products, or create a new prodcut.
    """

    if request.method == "GET":
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
    elif request.method == "POST":
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
def product_detail(request, pk):
    """
    Retrieve, update or delete a code product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = ProductSerializer(product).data
        return Response(data)
    elif request.method == "PATCH":
        serializer = UpdateProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
