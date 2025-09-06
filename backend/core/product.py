from core import database
import secrets

class ProductListingManager:
    def __init__(self, db: database.pymongo.database.Database):
        self.db = db

    def get_product_listing(self, product_id: str) -> dict | None:
        """
        Fetches product listing by product ID.
        """
        product = self.db["product_listings"].find_one({"product_id": product_id})
        if product is None:
            return None
        product.pop("_id", None)
        return product

    def update_product_listing(
            self,
            product_id: str,
            title: str | None = None,
            description: str | None = None,
            price: float | None = None,
            category: str | None = None,
            pictures: list[str] | None = None
        ) -> bool:
        """
        Updates product listing.
        """
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if price is not None:
            update_data["price"] = price
        if category is not None:
            update_data["category"] = category
        if pictures is not None:
            update_data["pictures"] = pictures
        result = self.db["product_listings"].update_one({"product_id": product_id}, {"$set": update_data})
        return result.modified_count > 0

    def create_product_listing(
            self,
            title: str,
            description: str,
            price: float,
            seller_email: str,
            category: str,
            pictures: list[str],
        ) -> bool:
        """
        Creates a new product listing.
        """
        product_data = {
            "product_id": secrets.token_hex(16),
            "title": title,
            "description": description,
            "price": price,
            "seller_email": seller_email,
            "category": category,
            "pictures": pictures or [],
            "created_at": database.datetime.datetime.utcnow()
        }
        result = self.db["product_listings"].insert_one(product_data)
        return result.acknowledged
    def delete_product_listing(self, product_id: str) -> bool:
        """
        Deletes a product listing.
        """
        result = self.db["product_listings"].delete_one({"product_id": product_id})
        return result.deleted_count > 0
    def search_product_listings(
            self,
            query: str,
            category: str | None = None,
            price_min: float | None = None,
            price_max: float | None = None,
            seller_email: str | None = None
        ) -> list[dict]:
        """
        Searches product listings by title or description.
        """
        results = self.db["product_listings"].find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        })
        filtered_results = []
        for result in results:
            match = True
            if category and result.get("category") != category:
                match = False
            if price_min is not None and result.get("price", 0) < price_min:
                match = False
            if price_max is not None and result.get("price", 0) > price_max:
                match = False
            if seller_email and result.get("seller_email") != seller_email:
                match = False
            if match:
                filtered_results.append(result)
        listings = []
        for product in filtered_results:
            product.pop("_id", None)
            listings.append(product)
        return listings
