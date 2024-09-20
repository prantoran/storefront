
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