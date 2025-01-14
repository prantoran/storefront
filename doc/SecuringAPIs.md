# Token-based authentication

After creating an user (using /user), authenticate using `/auth {username, password}`. If validated, the server returns a token as response.

Access gated APIs by adding the token in the request's header. The server will then validate the token and check expiry.

## DJoser

https://djoser.readthedocs.io/en/latest

RESTful impolementation of Django authentication system.

It provides a bunch of views for user registration, login, logut, password reset, and so on.

### Installation

Follow the latest instructions in the official doc.

```bash
pip install -U djoser
```

Djoser relies on an authentication engine/backend to perform the authentications. Djoser is just an API layer, a bunch of views, serializers and routes. 

### Auth engines
#### Token-based authentication
Built-in Django framework

Uses a db table to store tokens, i.e. incur a db call with every request to validate tokens.

#### JSON Web Token authentication
Seperate library

Every token has a digital signature which can be used to verify validity.

https://djoser.readthedocs.io/en/latest/authentication_backends.html#json-web-token-authentication

```bash
pip install -U djangorestframework_simplejwt
```

Root auth url: 127.0.0.1:8080/auth/users


# Add authentication endpoints

# Register, log in

# Apply permissions



