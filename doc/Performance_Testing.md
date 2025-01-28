
```python
python -m pip install locust
```

Identify core use cases.

```bash
 locust -f locustfiles/browse_products.py
```

# Optimizations

## Optimize the Python code
```python
# Preload related objects
Product.objects.select_related('...')
Product.objects.prefetch_related('...')

#Load only what is needed
Product.objects.only('title')
Product.objects.defer('description')

# Use values
Product.objects.values()
Product.objects.values_list()

# Count properly
Product.objects.count()
len(Product.objects.all()) # bad

# Bulk create/update
Product.objects.bulk_create([]) # send one instruction to create many
```

## Re-write the query

## Tune DB

indexes

## Cache the result

## Buy more hardware


# Profiling with Silk

[Silk](https://github.com/jazzband/django-silk) intercepts requests and responses and adds profiling information to the response.

Silk url: http://localhost:8000/silk/

Run performance tests with Locust and view the profiling information in Silk.

```bash
python -m pip install django-silk
```

```python
MIDDLEWARE += [
    ...
    'silk.middleware.SilkyMiddleware'
    ...
]

INSTALLED_APPS += ['silk']
```

## urls.py

```python
urlpatterns += [
    path('silk/', include('silk.urls', namespace='silk')),
]
```

## settings.py

```python
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_BINARY_DIR = os.path.join(BASE_DIR, 'silk-python-profiler')
```

## Management command

```bash
python manage.py migrate

# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, core, likes, sessions, silk, store, tags
# Running migrations:
#   Applying silk.0001_initial... OK
#   Applying silk.0002_auto_update_uuid4_id_field... OK
#   Applying silk.0003_request_prof_file... OK
#   Applying silk.0004_request_prof_file_storage... OK
#   Applying silk.0005_increase_request_prof_file_length... OK
#   Applying silk.0006_fix_request_prof_file_blank... OK
#   Applying silk.0007_sqlquery_identifier... OK
#   Applying silk.0008_sqlquery_analysis... OK
```

```bash
python manage.py collectstatic
```



# Baseline performance benchmark

## Simulating slow API
- http://httpbin.org/delay/2

```python
    @task(1)
    def slow_api(self):
        self.client.get("/playground/slow_api/")
```

```bash
locust -f locustfiles/browse_products.py
```
