from django.db.models.aggregates import Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view # not neeeded if using classed based views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # not needed if using view sets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView # Class-based view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .filters import ProductFilter
from .models import Cart, CartItem, Product, Collection, OrderItem, Review
from .pagination import DefaultPagination
from .serializers import CartItemSerializer, CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # filterset_fields = ['collection_id', 'unit_price']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     cid = self.request.query_params.get('collection_id')
    #     if cid is not None:
    #         queryset = queryset.filter(collection_id=cid)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({
                'error': 'Product cannot be deleted because it is associated with an order item.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)
    

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

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection=kwargs['pk']).count() > 0:
            return Response({
                'error': 'Collection cannot be deleted because it is associated with a product.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')
