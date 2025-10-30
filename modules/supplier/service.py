import re
from fastapi import HTTPException, status
from psycopg2 import IntegrityError

from modules.supplier.repository import SupplierRepository
from modules.supplier import schemas


class SupplierService:
    def get_suppliers(self):
        repository = SupplierRepository()
        return repository.get_all()


    def get_supplier_id(self, id:int):
        repository = SupplierRepository()
        return repository.get_id(id)


    def create_supplier(self, supplier:schemas.SupplierCreate):
        repository = SupplierRepository()

        # VALIDAR OS CAMPOS DO CREATE AQUI
        existing_company = repository.get_cnpj(supplier.cnpj)

        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Já existe uma empresa com o CNPJ {supplier.cnpj} cadastrado!'
            )
        
        if supplier.status not in ['ATIVO', 'INATIVO', 'SUSPENSO']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Status invãlido! Use ATIVO, INATIVO OU SUSPENSO'
            )
        
        pattern = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"
        if not re.match(pattern, supplier.cnpj):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ inválido! O formato correto é 00.000.000/0000-00"
            )

        try:
            return repository.save(supplier)
        except IntegrityError as e:
            if 'fk_supplier_company' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Empresa com id {supplier.company_id} não existe!'
                )

