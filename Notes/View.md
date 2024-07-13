A view function that takes a request and returns a response. 

View is a request handler.

We can use a view to pull data from db, transform data, send email, etc.

The views need to be connected to URLs using URLConf.
E.g. The view say_hello is connected in a local URLConf defined in urls.py which is then connected to the main URLConf in storefront/urls.py.