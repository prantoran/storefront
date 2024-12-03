from django.db.models.aggregates import Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view # not neeeded if using classed based views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # not needed if using view sets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView # Class-based view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from core import serializers
from store.permissions import IsAdminOrReadOnly
from .filters import ProductFilter
from .models import Cart, CartItem, Order, Product, Collection, OrderItem, Review, Customer, ProductImage
from .pagination import DefaultPagination
from .permissions import FullDjangoModelPermissions, ViewCustomerHistoryPermission
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, \
    CreatedOrderSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, ReviewSerializer, \
    UpdateCartItemSerializer, UpdateOrderSerializer, ProductImageSerializer


# Create your views here.


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()] # returning a list of objects, not permission classes 


    def create(self, request, *args, **kwargs):
        serializer = CreatedOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatedOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # Needed/useful when using CreateModelMixin
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # filterset_fields = ['collection_id', 'unit_price']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
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
    

class ProductImageViewSet(ModelViewSet):
    # serializer for /products/1(product_pk)/images/1(pk)
    # Extract product_pk and pass to serializer using context object
    # In the serializer
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    # queryset = Product.objects.all() # returns all product images
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])


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
    permission_classes = [IsAdminOrReadOnly]

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
    http_method_names = ['get', 'post', 'patch', 'delete']

    # serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')


class CustomerViewSet(ModelViewSet):
# class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [FullDjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    # permission_classes = [DjangoModelPermissions]
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]


    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)