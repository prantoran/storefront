We can use Django migrations to generate db schema from the models.

## Migrations

### Create
We create Django migrations to generate db tables based on the models in the project.

```bash
python manage.py makemigrations
```
When we run a migration against a db, Django will translate the classes generated in {appname}/migrations into SQL code and run it on top of the db.

### Run

```bash
python manage.py migrate
```
- Generates a `db.sqlite3` in project dir.

Auth table is used for authorizing and authenticating users.

Django uses 4 tables for its operations
- django_admin_log
- django_content_type
- django_migrations: Keeps track of the migrations applied to this db
- django_session


```bash
python manage.py migrate store 0003
```
- Show the actual SQL code executed at runtime.

### Reverse migrations
#### Opt 1: Undo the change and create a new migration

#### Opt 2: Completely revert the last migration
Downgrade the database to a previous migration.

```bash
# migrate to a previous migration number
python manage.py migrate store 0003
```

The code changes of the removed migrations will still reside in code, so they will be re-applied when we run `python manage.py migrate`. Hence, manually remove the changes from code. We can use git:
```bash
git log --oneline
git reset --hard HEAD~1
```

## Populating the db

```bash
python manage.py makemigrations store --empty
```

## Metadata

https://docs.djangoproject.com/en/5.0/ref/models/options

Define an inner class called Meta (name important) within the main model class.

## Generate or update DB schema using manual migrations

### Create a migration
```bash
python manage.py makemigrations store --empty
```

### Update operations in the created migration
i.e.
```json
    operations = [
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')
        """, """
            DELETE FROM store_collection
            WHERE title='collection1'
        """)
    ]
```
### Apply migration
```bash
python manage.py migrate
```

### Undo migration

```bash
python manage.py migrate store 0004
```

# Manager

Every model has an attribute called `objects`.
i.e. `Products.objects`

This is called a manager, an interface to the db.


# QuerySet
When we execute a manager's method, we get a QuerySet object. i.e. `query_set = Products.objects.all()`.

A QuerySet is an object that encapsulates a query. It is lazy (evaluated at a later point).

Django will execute a queryset under certain scenarios:
- We iterate over the queryset. i.e. `for p in query_set: `
- We convert it to a list. i.e. `list(query_set)`
- We access individual element. i.e. `query_set[0]`, `query_set[0:5]`


Operations on a queryset will return a new queryset. i.e. `query_set.filter().filter().order_by()`
