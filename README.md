
# StoreFront

An e-commerce backend developed with DJango using tutorial from [Programming with Mosh](https://www.youtube.com/watch?v=rHux0gMZ3Eg). 


## Setup

### Python environment
```bash
python -m venv venv
source venv/bin/activate
```

### Install Django
```bash
pip install django
```

### Start a new Django project
```bash
django-admin startproject storefront .
```


### Run 

#### server

```bash
python manage.py runserver 8080
```

#### MySQL
```bash
docker stop mysqlts; \
docker remove mysqlts; \
docker run --name mysqlts \
    -p 3306:3306/tcp -p 33060:33060/tcp \
    --network host \
    -v ~/ltsmysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_HOST=% \
    -e MYSQL_ROOT_PASSWORD=my-secret-pw \
    mysql:lts
```

#### SMTP Server
```bash
docker run --rm -it -p 5000:80 -p 2525:25 rnwood/smtp4dev
```

#### Redis
```bash
ocker run -d -p 6379:6379 redis
```
#### Celery
```bash
celery -A storefront beat
```

#### Locust
```bash
 locust -f locustfiles/browse_products.py
```

## Notes
Notes for different Django topics:
- [Admin App](/doc/Admin.md)
- [App](/doc/App.md)
- [Authentication](/doc/Authentication.md)
- [Database](/doc/DB.md)
- [Endpoints](/doc/Endpoints.md)
- [Database Functions](/doc/DB_Functions.md)
- [Django REST Framework](/doc/REST_Framework.md)
- [Debug](/doc/Debug.md)
- [Model](/doc/Model.md)
- [ORM](/doc/DjangoORM.md)
- [Template](/doc/Template.md)
- [View](/doc/View.md)
- [Automated Testing](/doc/Automated_Testing.md)