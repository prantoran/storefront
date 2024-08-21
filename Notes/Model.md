

## Create models
Using app
```python
python manage.py startapp store
python manage.py startapp tags
```

## Features
### One To One Field
`caustomer = models.OneToOneField(caustomer, on_delete=models.?, primary_key=[True,False])`

on_delete:
- models.CASCADE: delete when customer is deleted
- models.SET_NULL: object not deleted, Customer field is set to null when customer is deleted 
- models.SET_DEFAULT: object not deleted, Customer field is set to a default value
- models.PROTECT: cannot delete the parent because the object is associated

Django automatically creates an attribute in the Customer class for the object

# Expression Class
## Derived by
- Value
- F
- Func
- Aggregate