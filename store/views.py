from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView # Class-based view
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer
# Create your views here.

class ProductVViewSet(ModelViewSet)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({
                'error': 'Product cannot be deleted because it is associated with an order item.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer_class(self):
#     #     return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}



# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         s = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(s.data)
    
#     def post(self, request):
#         s = ProductSerializer(data=request.data)
#         s.is_valid(raise_exception=True)
#         s.save()
#         return Response(s.data, status=status.HTTP_201_CREATED)
    

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         s = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(s.data)
#     elif request.method == 'POST': 
#         s = ProductSerializer(data=request.data)
#         # if s.is_valid():
#         #     s.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
#         s.is_valid(raise_exception=True)
#         s.save()
#         print(s.validated_data)
#         return Response(s.data, status=status.HTTP_201_CREATED)


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'id' # by default, it is pk
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({
#                 'error': 'Product cannot be deleted because it is associated with an order item.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         s = ProductSerializer(product, context={'request': request})
#         return Response(s.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         s = ProductSerializer(product, data=request.data)
#         s.is_valid(raise_exception=True)
#         s.save()
#         return Response(s.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({
#                 'error': 'Product cannot be deleted because it is associated with an order item.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     # try:
#     #     p = Product.objects.get(pk=id)
#     #     s = ProductSerializer(p)
#     #     return Response(s.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({
#                 'error': 'Product cannot be deleted because it is associated with an order item.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         if request.method == 'GET':
#             s = ProductSerializer(product, context={'request': request})
#         elif request.method == 'PUT':
#             s = ProductSerializer(product, data=request.data)
#             s.is_valid(raise_exception=True)
#             s.save()
#         return Response(s.data)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        
        if collection.products.count() > 0:
            return Response({
                'error': 'Collection cannot be deleted because it is associated with a product.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer


# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).select_related('featured_product').all()
#         s = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(s.data)
#     elif request.method == 'POST': 
#         s = CollectionSerializer(data=request.data)
#         s.is_valid(raise_exception=True)
#         s.save()
#         return Response(s.data, status=status.HTTP_201_CREATED)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#             products_count=Count('products'))
#     serializer_class = CollectionSerializer
    
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
        
#         if collection.products.count() > 0:
#             return Response({
#                 'error': 'Collection cannot be deleted because it is associated with a product.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#             products_count=Count('products')), pk=pk)
#     if request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({
#                 'error': 'Collection cannot be deleted because it is associated with a product.'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         if request.method == 'GET':
#             s = CollectionSerializer(collection, context={'request': request})
#         elif request.method == 'PUT':
#             s = CollectionSerializer(collection, data=request.data)
#             s.is_valid(raise_exception=True)
#             s.save()
#         return Response(s.data)