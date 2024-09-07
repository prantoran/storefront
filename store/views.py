from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        s = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(s.data)
    elif request.method == 'POST': 
        s = ProductSerializer(data=request.data)
        # if s.is_valid():
        #     s.validated_data
        #     return Response('ok')
        # else:
        #     return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        s.is_valid(raise_exception=True)
        print(s.validated_data)
        return Response('ok')


@api_view()
def product_detail(request, id):
    # try:
    #     p = Product.objects.get(pk=id)
    #     s = ProductSerializer(p)
    #     return Response(s.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    p = get_object_or_404(Product, pk=id)
    s = ProductSerializer(p, context={'request': request})
    return Response(s.data)


@api_view()
def collection_detail(request, pk):
    return Response('ok')