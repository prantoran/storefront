from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

@api_view()
def product_list(request):
    queryset = Product.objects.all()
    s = ProductSerializer(queryset, many=True)
    return Response(s.data)


@api_view()
def product_detail(request, id):
    # try:
    #     p = Product.objects.get(pk=id)
    #     s = ProductSerializer(p)
    #     return Response(s.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    p = get_object_or_404(Product, pk=id)
    s = ProductSerializer(p)
    return Response(s.data)
