import time
from core import database

class Orders:
    def __init__(self, db: database.pymongo.database.Database):
        self.db = db

    def create_order(self, email: str, products: list[str]) -> bool:
        """
        Creates a new order for the user.
        """
        result = self.db["orders"].insert_one({
            "email": email,
            "products": products,
            "created_at": time.time(),
        })
        return result.acknowledged

    def get_orders(self, email: str) -> list[dict]:
        """
        Fetches all orders for the user.
        """
        results = self.db["orders"].find({"email": email})
        orders = []
        for order in results:
            order.pop("_id", None)
            order.pop("email", None)
            orders.append(order)
        return orders
