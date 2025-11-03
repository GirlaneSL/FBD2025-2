from itertools import product
from fastapi import HTTPException, status
from psycopg2 import IntegrityError

from modules.product.repository import ProductRepository
from modules.product.schemas import ProductCreate


class ProductService:
    def get_products(self):
        repository = ProductRepository()
        products = repository.get_all()

        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não há produtos cadastrados!'
            )

        return products
    

    def get_product_id(self, id:int):
        repository = ProductRepository()
        product = repository.get_id(id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Produto com id {id} não existe!'
            )

        return product


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
                    detail=f'Fornecedor com id {product.supplier_id} não existe!'
                )
            if 'fk_product_company' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Empresa com id {product.company_id} não existe!'
                )
    

    def get_products_company_id(self, company_id:int):
        repository = ProductRepository()
        company_products = repository.get_company_id(company_id)

        if not company_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Não há produtos da empresa com id {company_id}!'
            )

        return company_products
        