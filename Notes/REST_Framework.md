
A separate framework on top of Django.

```bash
pip install djangorestframework
```

| Django        | REST Framework    |
| ------------- | ----------------- |
| HttpRequest   | Request           |
| HttpResponse  | Response          |


# Serializer

Converts a model instance to a dictionary

## Serializing Relationships
- Primary key
- String
- Nested object
- Hyperlink


## Model Serializer

For a related field within model, by default we get primary key for the related field using MS.

We can use `"__all__"` for fields to include all fields of a model, but this is bad practice as this does not separate internal and external representation of a model.

# Class-based views
Using classes, instead of functions, to define views for REST methods.
## Benefits of class-based views
- Less messy, fewer conditional statements.

# Mixins

Set of reusable common statements packed together.

## Generic views

Concrete class that implements one or two mixins.

## View Sets

Combine the logic of multiple related views inside a single class

We cannot use explicit url patterns with view sets. We need routers. We register a view set with a router and the router will take care of generating the url patterns.

# Building the API
- Create a serializer
- Create a view
- Register a route

# Nested routers

```bash
pip install drf-nested-routers
```


# Generic filtering

```bash
pip install django-filter
```

## Add package in settings
```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
}
```

## Create Filter class in filter.py

```python
from django_filters.rest_framework import FilterSet
from .models import Product



class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }
```

## Add filter to views

```python
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    # filterset_fields = ['collection_id', 'unit_price']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     cid = self.request.query_params.get('collection_id')
    #     if cid is not None:
    #         queryset = queryset.filter(collection_id=cid)
    #     return queryset
    ...
```

# Searching & Ordering

In store/views.py,

```python
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductViewSet(ModelViewSet):
    filter_backends = [..., SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    ...
```
