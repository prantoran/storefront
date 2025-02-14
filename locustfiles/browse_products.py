from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    # locust will create instances of this class for each user and run tasks in this class
    # Viewing product details
    # Add product to cart
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        print('View products')
        collection_id = randint(2, 6)
        self.client.get(
            f"/store/products/?collection_id={collection_id}/",
            name="/store/products")

    @task(4)
    def view_product(self):
        print('View product details')
        product_id = randint(1, 1000)
        self.client.get(
            f"/store/products/{product_id}/",
            name="/store/products/:id")

    @task(4)
    def add_to_cart(self):
        print("Add to cart")
        product_id = randint(1, 10)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            name="/store/carts/items/",
            json={"product_id": product_id, "quantity": 1}
        )

    @task(4)
    def slow_api(self):
        self.client.get("/playground/slow_api/", name="/playground/slow_api/")

    def on_start(self):
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
