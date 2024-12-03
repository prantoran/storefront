# Uploading files using nested URLs

We need serializer, view and router to implement an endpoint.

serializer for /products/1(product_pk)/images/1(pk)

Extract product_pk and pass to serializer using context object

In the serializer, extract product_pk from the context object to create a ProductImage object.