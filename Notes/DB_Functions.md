The database functions are common in all database engines. 

The DEs have their own custom functions that can be used using F().



Concat()

```python
from django.db.models.functions import Concat

full_name=Concat('first_name', Value(' '), 'last_name')
```