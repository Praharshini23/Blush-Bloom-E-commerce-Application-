from locust import HttpUser, task, between
import random

class MakeupShopCustomer(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Each simulated visitor starts a session by submitting the demo login form.
        self.client.post("/", data={"name": f"Test User {random.randint(1,99999)}",
                                    "email": f"test{random.randint(1,99999)}@example.com"},
                         name="/login")

    @task(5)
    def browse_home(self):
        self.client.get("/home", name="/home")

    @task(3)
    def search(self):
        self.client.get(f"/home?q={random.choice(['lip','face','glow','rose'])}", name="/home search")

    @task(3)
    def view_product(self):
        self.client.get(f"/product/{random.randint(1,8)}", name="/product/[id]")

    @task(2)
    def add_to_bag_and_view_cart(self):
        product_id = random.randint(1,8)
        self.client.post(f"/cart/add/{product_id}", name="/cart/add")
        self.client.get("/cart", name="/cart")
