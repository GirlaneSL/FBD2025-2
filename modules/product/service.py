from fastapi import HTTPException, status
from psycopg2 import IntegrityError

from modules.product.repository import ProductRepository
from modules.product.schemas import ProductCreate


class ProductService:
    def get_products(self):
        repository = ProductRepository()
        return repository.get_all()
    

    def get_product_id(self, id:int):
        repository = ProductRepository()
        return repository.get_id(id)


    def create_product(self, product:ProductCreate):
        repository = ProductRepository()
         
        try:
            return repository.save(product)
        except IntegrityError as e:
            if 'fk_product_type' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Tipo de produto com id {product.type_id} não existe!'
                )
            if 'fk_product_supplier' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Forneceor com id {product.supplier_id} não existe!'
                )
            if 'fk_product_company' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Empresa com id {product.company_id} não existe!'
                )
    

    def get_products_supplier_type(self, company_id:int):
        repository = ProductRepository()
        return repository.get_company_products(company_id)
        