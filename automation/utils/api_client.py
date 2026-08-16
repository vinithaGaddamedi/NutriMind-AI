import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url

    def get_products(self):
        return requests.get(f"{self.base_url}/products")

    def add_to_cart(self, user_id, product_id, quantity=1):
        return requests.post(f"{self.base_url}/cart/", json={
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        })

    def get_cart(self, user_id):
        return requests.get(f"{self.base_url}/cart/{user_id}")

    def create_order(self, user_id):
        return requests.post(f"{self.base_url}/order/", json={"user_id": user_id})

    def get_recommendations(self, user_id):
        return requests.get(f"{self.base_url}/recommendations/{user_id}")
