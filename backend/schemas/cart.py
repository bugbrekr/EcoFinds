from pydantic import BaseModel

class CartItem(BaseModel):
    product_id: int
    quantity: int

class AddToCartRequest(BaseModel):
    product_id: int

class RemoveFromCartRequest(BaseModel):
    product_id: int