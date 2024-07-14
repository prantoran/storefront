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


## Metadata

https://docs.djangoproject.com/en/5.0/ref/models/options

Define an inner class called Meta (name important) within the main model class.
