from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction, connection
from django.db.models import Q, DecimalField
from django.db.models import F, Func, Value, ExpressionWrapper # Expression classes
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, OrderItem, Order, Customer, Collection, Cart, CartItem
from tags.models import TaggedItem
# Create your views here.


def attach_file(request):
    try:
        email = EmailMessage(
            'subject',
            'message',
            'prantoran@gmail.com',
            ['zerotounite007@gmail.com'])
        email.attach_file('playground/static/test.txt')
        email.send()
    except BadHeaderError as err:
        print("Bad header error: ", err)
        pass
    return HttpResponse('Email sent')


def mail_admin(request):
    try:
        mail_admins(
            'subject',
            'message',
            fail_silently=False,
            html_message='message'
        )
    except BadHeaderError as err:
        print("Bad header error: ", err)
        pass
    return HttpResponse('Email sent')

def say_hello(request):
    # queryset = Product.objects.all()
    # for p in queryset:
    #     print(p)

    # try:
    #     product = Product.objects.get(id=1)
    #     product = Product.objects.get(pk=1) # primary_key, auto-resolved
    # except ObjectDoesNotExist:
    #     pass

    # product = Product.objects.filter(pk=0).first() # None if does not exists

    # exists = Product.objects.filter(pk=0).exists() # None if does not exists

    # # Products: inventory < 10 AND price < 20
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # # Products: inventory < 10 AND price < 20
    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | ~Q(unit_price__lt=20))

    # # Products: inventory = price
    # queryset = Product.objects.filter(inventory=F('unit_price'))
    # # Compare with a field in a related table
    # queryset = Product.objects.filter(inventory=F('collection__id'))

# ----------------
    # # sorting
    # queryset = Product.objects.order_by('unit_price', '-title').reverse()
    # product = Product.objects.order_by('unit_price')[0]
    # product_cheapest = Product.objects.earliest('unit_price')
    # product_priciest = Product.objects.latest('unit_price')

    # # limiting results
    # queryset = Product.objects.all()[5:12]

    # # select
    # queryset = Product.objects.values('id', 'title', 'unit_price', 'collection__title') # returns array of dicts
    # queryset = Product.objects.values_list('id', 'title', 'unit_price', 'collection__title')

    # queryset = Product.objects.filter(
    #     id__in=OrderItem.objects.values('product__id').distinct().order_by('title')
    # )
    # return HttpResponse('Hello World')
    # return render(request, 'hello.html', { 'name': 'Goku', 'products': list(queryset), 'cheapest': product_cheapest })
# ----------------

# ---------------- Deferring fields
    # queryset = Product.objects.only('id', 'title')
    # queryset = Product.objects.defer('description') # defer the loading of certain fields later
    # return render(request, 'hello.html', { 'name': 'Goku', 'products': list(queryset) })
# ----------------

#----------------- Selecting related objects
    # queryset = Product.objects.select_related('collection').all() # (1) instance of collection per product; Preload, creates a join between tables
    # queryset = Product.objects.prefetch_related('promotions').all() # (n) instances of promotions per product;

    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # return render(request, 'hello.html', { 'name': 'Goku', 'products': list(queryset) })
# ----------------
# ---------------- Sending email
    print("received request")
    try:
        mail_admins(
            'subject',
            'message',
            fail_silently=False,
            html_message='message'
        )
        # send_mail(
        #     'subject',
        #     'message',
        #     'prantoran@gmail.com',
        #     ['zerotounite007@gmail.com'])
    except BadHeaderError as err:
        print("Bad header error: ", err)
        pass
    return render(request, 'hello.html', { 'name': 'Goku'})



def last_five(request):
    # Get the last 5 orders with their customers and items (incl product)
    queryset = Order.objects.prefetch_related('orderitem_set__product').select_related('customer').order_by('-placed_at')[:5]
    return render(request, 'hello.html', { 'name': 'Goku', 'orders': list(queryset) })

def aggregate(request):
    result = Product.objects.filter(collection__id=1).aggregate(
        products_count=Count('id'), min_price=Min('unit_price'))
    return render(request, 'hello.html', { 'name': 'Goku', 'agg_count_result': result })

def annotate(request):
    # Setting a new field is_new and setting to True using an expression object (cannot directly set is_new=True).
    # F('id')) references the id field in the customer record
    queryset = Customer.objects.annotate(
        is_new=Value(True), 
        new_id=F('id') + 1,
        full_name=Func(F('first_name'), Value(' '),
                        F('last_name'), function='CONCAT'),
        full_name_alt=Concat('first_name', Value(' '), 'last_name'),
        orders_count=Count('order')
    )
    return render(request, 'hello.html', { 'name': 'Goku', 'annotate_result': list(queryset)})

    '''
    Executed SQL query:
    SELECT `store_customer`.`id`,
        `store_customer`.`first_name`,
        `store_customer`.`last_name`,
        `store_customer`.`email`,
        `store_customer`.`phone`,
        `store_customer`.`birth_date`,
        `store_customer`.`membership`,
        1 AS `is_new`,
        (`store_customer`.`id` + 1) AS `new_id`,
        CONCAT(`store_customer`.`first_name`, ' ', `store_customer`.`last_name`) AS `full_name`,
        CONCAT_WS('', `store_customer`.`first_name`, CONCAT_WS('', ' ', `store_customer`.`last_name`)) AS `full_name_alt`,
        COUNT(`store_order`.`id`) AS `orders_count`
    FROM `store_customer`
    LEFT OUTER JOIN `store_order`
        ON (`store_customer`.`id` = `store_order`.`customer_id`)
    GROUP BY `store_customer`.`id`,
            9,
            10,
            11
    ORDER BY NULL
    '''

def annotate_product(request):
    queryset = Product.objects.annotate(
        discounted_price=ExpressionWrapper(
            F('unit_price') * 0.8, output_field=DecimalField()
        )
    )
    return render(request, 'hello.html', { 'name': 'Goku', 'annotate_product_result': list(queryset)})

def annotate_practice(request):
    # Customers with their last order ID
    qs1 = Customer.objects.annotate(last_order_id=Max('order__id'))
    # Collections and count of their products  
    qs2 = Collection.objects.annotate(products_count=Count('product'))
    # Customers with more than 5 orders
    qs3 = Customer.objects \
        .annotate(orders_count=Count('order')) \
        .filter(orders_count__gt=5)
    # Customers and the total amount they’ve spent 
    qs4 = Customer.objects.annotate(
        total_spent=Sum(
            F('order__orderitem__unit_price') *
            F('order__orderitem__quantity')
        )
    )
    # Top 5 best-selling products and their total sales
    qs5 = Product.objects.annotate(
        total_sales=Sum(
            F('orderitem__unit_price') *
            F('orderitem__quantity')
        )
    ).order_by('-total_sales')[:5]
    
    return render(request, 'hello.html', {
        'name': 'Goku', 
        'qs1': list(qs1),
        'qs2': list(qs2),
        'qs3': list(qs3),
        'qs4': list(qs4),
        'qs5': list(qs5)
    })

def contenttype(request):
    content_type = ContentType.objects.get_for_model(Product)

    qs = TaggedItem.objects \
        .select_related('tag') \
        .filter(
            content_type=content_type,
            object_id=1
    )

    return render(request, 'hello.html', {'name': 'Nobody', 'tags': list(qs) })

# same as contenttype, but using a customer manager in tags/models.py
def taggeditem_custom_manager(request):
    qs = TaggedItem.objects.get_tags_for(Product, 1)
    return render(request, 'hello.html', {'name': 'Nobody', 'tags': list(qs) })

def create_collection(request):
    c = Collection()
    c.title = 'Video Games'
    c.featured_product = Product(pk=1)
    # c.featured_product_id = 1
    c.save()

    Collection.objects.create(title='a', featured_product_id=1)


    return render(request, 'hello.html', {'name': 'Father?:(' })


def update_collection(request):
    c = Collection.objects.get(pk=11)
    c.title = 'Yo'
    c.featured_product = Product(pk=1)
    c.save()

    Collection.objects.filter(pk=12).update(featured_product_id=None, title='foo')

    return render(request, 'hello.html', {'name': 'Father?:(' })


def delete_collection(request):
    c = Collection(pk=11)
    c.delete()

    Collection.objects.filter(id__gt=12).delete()

    return render(request, 'hello.html', {'name': 'Father?:(' })


def cart_create(request):
    # create a shopping cart with an item
    c = Cart()
    c.save()

    ca = CartItem()
    ca.cart = c
    ca.product_id = 1
    ca.quantity = 1
    ca.save()

    return render(request, 'hello.html', {'name': 'Goku'})


def cart_update(request):
    # update the quantity of an item
    ca = CartItem.objects.get(pk=1)
    ca.quantity = 9
    ca.save()

    return render(request, 'hello.html', {'name': 'Goku'})


def cart_delete(request):
    # remove a cart
    c = Cart(pk=1)
    c.delete()
    # because cascading is enabled in the relationships between
    # cart and its items, deleting a cart automatically causes
    # deletion of its items

    return render(request, 'hello.html', {'name': 'Goku'})


# @transaction.atomic
def order_transaction(request):
    with transaction.atomic():
        o = Order()
        o.customer_id = 1
        o.save()

        oi = OrderItem()
        oi.order = o
        oi.product_id = 1
        oi.quantity = 1
        oi.unit_price = 1009
        oi.save()

    return render(request, 'hello.html', {'name': 'Goku'})


def raw_sql(request):
    raw_qs = Product.objects.raw('SELECT * FROM store_product')

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM store_customer')
    cursor.close()

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_order')
        # execute stored procedures
        # cursor.callproc('get_customers', [1, 2, 3])

    return render(request, 'hello.html', {'name': 'Goku', 'raw_sql': list(raw_qs)})