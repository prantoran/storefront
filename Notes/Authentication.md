
# Change user model

Always create a custom user model at the beginning of a project because it is much harder to change user models in the middle of the project.

To make changes to user model in the middle of project, the simplest solution is to drop db and migrate fresh.

## Reset db

```sql
DROP DATABASE storefront2;
CREATE DATABASE storefront2;
```

## Migrate
```python
python manage.py makemigrations
python manage.py migrate
```
## Setting up Admin panel

```python
python manage.py createsuperuser
```
http://127.0.0.1:8080/admin

# Composition

## Extend User

User

    ^
    |

AppUser

- For storing attributes related to authentication



## Create Profile


Profile -> User

- For storing non-auth related attributes


# Groups

A group is a collectionf of permissions.

Create groups from the admin panel and assign groups in user's panel.

## Custom permissions

e.g.
store/models.py

```python
class Order:
    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]
```

```bash
python manage.py makemigrations
python manage.py migrate
```

Creates a record in `auth_permissions` table in the Django db for the project.


# Create user

Default serializer used Djoser: 'user_create': 'djoser.serializers.UserCreateSerializer',

'user_create': 'djoser.serializers.UserCreateSerializer'


# Logging in

## JWT token
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest


### Create

```bash
localhost:8080/auth/jwt/create
```

401 Unauthorized for wrong credentials (user, password)


response after valid cred:

```json
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "refresh": "...",
    "access": "..."
}
```

Access token is valid for 1 day and access token is valid for 5 minutes by default. The times can be changed by modifying keys of SIMPLE_JWT.

### Refresh access token

```bash
http://127.0.0.1:8080/auth/jwt/refresh
```

# Getting the current user

```bash
http://127.0.0.1:8080/auth/users/me/
```
Add JWT auth token using extensions, such as [ModHeader](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj) from Chrome.

Header key: `Authorization`
value: `JWT`{access_token}
- We add the JWT prefix because we defined so in settings.py::SIMPLE_JWT.AUTH_HEADER_TYPEs

# Getting current user's profile

```bash
http://127.0.0.1:8080/store/customers/me/
```

# Permissions

https://www.django-rest-framework.org/api-guide/permissions