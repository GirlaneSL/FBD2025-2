from typing import Optional
from fastapi import APIRouter

from modules.product import schemas
from modules.product.service import ProductService

router = APIRouter(prefix='/produto', tags=['Products'])


@router.get('/', response_model=list[schemas.ProductResponse])
def list_products():
    service = ProductService()
    return service.get_products()


@router.get('/{id}', response_model=Optional[schemas.ProductResponse])
def get_product_by_id(id:int):
    service = ProductService()
    return service.get_product_id(id)


@router.post('/', response_model=schemas.Product)
def add_product(product:schemas.ProductCreate):
    service = ProductService()
    return service.create_product(product)


@router.get('/empresa/{company_id}/produtos', response_model=list[schemas.ProductResponse])
def get_products_by_supplier_and_type(company_id:int):
    service = ProductService()
    return service.get_products_supplier_type(company_id)