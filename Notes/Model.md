

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
- ExpressionWrapper


# Building the model
- Create a model class
- Create a migration
```bash
python manage.py makemigrations
```
- Apply the migration
```bash
python manage.py migrate
```

# GUID
Globally unique identifier
32 char string

We should use GUID show that the IDs are hard to predict.

```python
from uuid import uuid4

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
```

# Add unique constraint
 
```python
class CartItem(models.Model):
    class Meta:
        unique_together = [['cart', 'product']]  # needed for incrementing product qty for a cart instead of creating a new (cart, product) record
```


# Signals

Notifications/messages

- pre_save

Sent when a model is saved.

- post_save

After a model is saved.

- pre_delete

When a model is deleted.

- post_delete

After a model is deleted.

We can listen to these notifications and change state.
i.e. Get notified when a user is created.