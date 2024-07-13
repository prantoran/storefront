
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


### Run server

```bash
mython manage.py runserver 8080
```


## Create apps
Defined in storefront/settings.py 
Preconfigured apps:
- admin: Admin interface for managing data
- auth: Authenticate users
- contenttypes: 
- sessions: [legacy] Temporary memory in server for managing user sessions
- messages: For displaying one-time notification to the user
- staticfiles: For serving static files