from core import database

class CartManager:
    def __init__(self, db: database.pymongo.database.Database):
        self.db = db

    def add_to_cart(self, email: str, product_id: str) -> bool:
        """
        Adds a product to the user's cart.
        """
        result = self.db["carts"].update_one(
            {"email": email},
            {"$addToSet": {
                "products": product_id
            }},
            upsert=True
        )
        return result.acknowledged

    def remove_from_cart(self, email: str, product_id: str) -> bool:
        """
        Removes a product from the user's cart.
        """
        result = self.db["carts"].update_one(
            {"email": email, "product_id": product_id},
            {"$pull": {
                "products": product_id
            }}
        )
        return result.modified_count > 0

    def get_cart_items(self, email: str) -> list[dict]:
        """
        Fetches all items in the user's cart.
        """
        results = self.db["carts"].find({"email": email})
        cart_items = []
        for item in results:
            item.pop("_id", None)
            cart_items.append(item)
        return cart_items

    def clear_cart(self, email: str) -> bool:
        """
        Clears the user's cart.
        """
        self.db["carts"].update_one(
            {"email": email},
            {"$set": {"products": []}}
        )
        return True
