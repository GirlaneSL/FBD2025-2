from modules.company import schemas
from modules.company.repository import CompanyRepository

import re

from fastapi import HTTPException, status


class CompanyService:
    def get_companies(self):
        repository = CompanyRepository()
        companies = repository.get_all()

        if not companies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não há produtos cadastrados!'
            )

        return companies


    def create_company(self, company: schemas.CompanyCreate):
        repository = CompanyRepository()

        # VALIDAR OS CAMPOS DO CREATE AQUI
        existing_company = repository.get_cnpj(company.cnpj)

        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Já existe uma empresa com o CNPJ {company.cnpj} cadastrado!'
            )
        
        if company.status not in ['ATIVO', 'INATIVO', 'SUSPENSO']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Status invãlido! Use ATIVO, INATIVO OU SUSPENSO'
            )
        
        pattern = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"
        if not re.match(pattern, company.cnpj):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ inválido! O formato correto é 00.000.000/0000-00"
            )

        return repository.save(company)


    def get_company_id(self, id: int):
        repository = CompanyRepository()
        company = repository.get_id(id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Empresa com id {id} não existe!'
            )

        return company
