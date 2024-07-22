from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product

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

    # return HttpResponse('Hello World')
    return render(request, 'hello.html', { 'name': 'Goku', 'products': list(queryset)})