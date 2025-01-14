## Create a custom app
Defined in storefront/settings.py 
Preconfigured apps:
- admin: Admin interface for managing data
- auth: Authenticate users
- contenttypes: 
- sessions: [legacy] Temporary memory in server for managing user sessions
- messages: For displaying one-time notification to the user
- staticfiles: For serving static files

### Create

```bash
python manage.py startapp playground
```

#### Structure
- Migrations/
- admin.py: Defines the admin interface
- apps.py: Configures the app
- models.py: Model classes to pull out data from the database and present to users
- tests.py: Unit tests
- views.py: 

### Register
Add the app to settings.py/INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'playground'
]
```