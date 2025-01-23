
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