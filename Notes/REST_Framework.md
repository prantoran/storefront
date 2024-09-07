
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