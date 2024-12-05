from storefront.settings import INSTALLED_APPS

# Uploading files using nested URLs

We need serializer, view and router to implement an endpoint.

serializer for /products/1(product_pk)/images/1(pk)

Extract product_pk and pass to serializer using context object

In the serializer, extract product_pk from the context object to create a ProductImage object.


## CORS

Cross-origin Resource Sharing

### [django-cors-headers](https://pypi.org/project/django-cors-headers)

```bash
python -m pip install django-cors-headers
```

```python
INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
]
```

```python
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]
```

Configure the middleware’s behaviour in your Django settings. You must set at least one of three following settings:
- CORS_ALLOWED_ORIGINS
- CORS_ALLOWED_ORIGIN_REGEXES
- CORS_ALLOW_ALL_ORIGINS