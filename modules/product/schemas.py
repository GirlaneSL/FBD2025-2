from pydantic import BaseModel

from modules.type_product.schemas import TypeProduct
from modules.supplier.schemas import SupplierResponse


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    type_id: int
    supplier_id: int
    company_id: int


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    type_id: int
    supplier_id: int
    company_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    type: TypeProduct
    supplier: SupplierResponse
    company_id: int


class ProductSimple(BaseModel):
    name: str
 