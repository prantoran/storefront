from decimal import Decimal
from wsgiref import validate
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']
    
    products_count = serializers.IntegerField()


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