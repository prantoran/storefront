from dataclasses import field
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']
    
    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'price', 'price_with_tax', 'collection'] # '__all__'
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    # # collection = serializers.PrimaryKeyRelatedField(
    # #     queryset = Collection.objects.all()
    # # )
    # # collection = serializers.StringRelatedField()
    # # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1) 
    
    # # overriding the create/save
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('price')
    #     instance.save()
    #     return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([u.quantity * u.product.unit_price for u in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            # update an item
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item # following the same pattern for ModelSerializer::save()
        except CartItem.DoesNotExist:
            # create an item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
    
        return self.instance # following the same pattern for ModelSerializer::save()


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True) # user_id is created dynamically at runtime but we need this when updating user with phone, etc
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    # We will use the Meta class, so we are inheriting ModelSerializer
    class Meta:
        model = Order
        fields = ['payment_status']


class CreatedOrderSerializer(serializers.Serializer):
    # we are not inheriting from ModelSerializer because Order model does not have the cart_id field

    with transaction.atomic():
        cart_id = serializers.UUIDField()

        def validate_cart_id(self, cart_id):
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError(
                    'No cart with the given ID was found.')
            if CartItem.objects.filter(cart_id=cart_id).count() == 0:
                raise serializers.ValidationError('The cart is empty.')
            return cart_id


        def save(self, **kwargs):
            cart_id = self.validated_data['cart_id']

            (customer, created) = Customer.objects.get_or_create(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                            .select_related('product') \
                            .filter(cart_id=cart_id) # get a queryset
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price,
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=cart_id).delete()

            return order