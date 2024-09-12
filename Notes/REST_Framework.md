
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