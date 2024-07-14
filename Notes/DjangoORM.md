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


## Populating the db