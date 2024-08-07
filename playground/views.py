from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product, OrderItem

# Create your views here.

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

    # # sorting
    # queryset = Product.objects.order_by('unit_price', '-title').reverse()
    # product = Product.objects.order_by('unit_price')[0]
    product_cheapest = Product.objects.earliest('unit_price')
    # product_priciest = Product.objects.latest('unit_price')

    # # limiting results
    # queryset = Product.objects.all()[5:12]

    # # select
    # queryset = Product.objects.values('id', 'title', 'unit_price', 'collection__title') # returns array of dicts
    queryset = Product.objects.values_list('id', 'title', 'unit_price', 'collection__title')

    queryset = Product.objects.filter(
        id__in=OrderItem.objects.values('product__id').distinct().order_by('title')
    )
    # return HttpResponse('Hello World')
    return render(request, 'hello.html', { 'name': 'Goku', 'products': list(queryset), 'cheapest': product_cheapest })