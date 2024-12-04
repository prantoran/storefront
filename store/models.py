from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

from store import permissions
from store.validators import validate_file_size


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    
    # product_set: 
    # all the products the promotion is applied
    # automatically created by Django

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    # change the str rep of objects
    def __str__(self) -> str:
        return self.title.__str__()
    
    class Meta:
        ordering = ['title']


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255) # varchar 255
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits = 6, 
        decimal_places = 2,
        validators = [
            MinValueValidator(1, message="Unit price has to be >= 1.0")
        ]
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, related_name='product_set', blank=True)

    def __str__(self) -> str:
        return self.title.__str__()
    
    class Meta:
        ordering = ['title']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='images')
    image = models.ImageField(
        upload_to='store/images', # Relative to te MEDIA_ROOT defined in settings.py
        validators=[validate_file_size]
    )


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]

    # already exists in user model
    # first_name = models.CharField(max_length=255) 
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    # order_set automatically created because Order class has Customer as a foreign key
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        # db_table = 'store_customer'
        # indexes = [
        #     models.Index(fields=['last_name', 'first_name'])
        # ]
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(models.Model):
    PAYSTATUS_PENDING = 'P'
    PAYSTATUS_COMPLETE = 'C'
    PAYSTATUS_FAILED = 'F'

    PAYSTATUS_CHOICES = [
        (PAYSTATUS_PENDING, 'PENDING'),
        (PAYSTATUS_COMPLETE, 'COMPLETE'),
        (PAYSTATUS_FAILED, 'FAILED')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYSTATUS_CHOICES, default=PAYSTATUS_PENDING)

    # 1 to many
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    
    # 1 to 1 
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

    # 1 to many
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') # replace related_name default ('cartitem_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]  # needed for incrementing product qty for a cart instead of creating a new (cart, product) record


class Review(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)