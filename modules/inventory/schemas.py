from datetime import date
from pydantic import BaseModel

from modules.product.schemas import ProductSimple


class Inventory(BaseModel):
    id: int
    product_id: int
    quantity: int
    update_date: date


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int


class InventotyResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductSimple
    update_date: date
