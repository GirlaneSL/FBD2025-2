import re
from psycopg2 import IntegrityError
from fastapi import HTTPException, status

from modules.type_product.repository import TypeProductRepostiroy
from modules.type_product import schemas


class TypeProductService:
    def get_type_products(self):
        repository = TypeProductRepostiroy()
        return repository.get_all()


    def get_type_product_id(self, id:int):
        repository = TypeProductRepostiroy()
        return repository.get_id(id)
    
    
    def create_type_product(self, type_product:schemas.TypeProductCreate):
        repository = TypeProductRepostiroy()
        
        existing_type_product = repository.get_cod(type_product.cod_type)

        if existing_type_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Já existe um tipo com o código {type_product.cod_type} cadastrado!'
            )
        
        pattern = r'^[A-Z]{2}-\d{3}$'
        if not re.match(pattern, type_product.cod_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Código inválido! O formato correto é XX-000'
            )
        
        try:
            return repository.save(type_product)
        except IntegrityError as e:
            if 'fk_type_product_company' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Empresa com id {type_product.company_id} não existe!'
                )
