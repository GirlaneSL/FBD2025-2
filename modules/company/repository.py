from fastapi import params
from core.db import DataBase
from modules.company.schemas import CompanyCreate


class CompanyRepository:
    QUERY_COMPANIES = 'SELECT id, name FROM company'
    QUERY_COMPANY_ID = 'SELECT id, name FROM company where id = %s'
    QUERY_CREATE_COMPANY = 'INSERT INTO company (name, cnpj, status) VALUES (%s, %s, %s) RETURNING id'
    QUERY_COMPANY_CNPJ = 'SELECT id, name, cnpj, status FROM company WHERE cnpj = %s'


    def get_all(self):
        db = DataBase()
        companies = db.execute(self.QUERY_COMPANIES)
        results = []
        for company in companies:
            results.append({
                'id': company[0], 
                'name': company[1]})
        return results


    def save(self, company: CompanyCreate):
        db = DataBase()
        query = self.QUERY_CREATE_COMPANY
        params = (company.name, company.cnpj, company.status)
        result = db.commit(query, params)
        return {
            'id': result[0],
            'name': company.name,
            'cnpj': company.cnpj,
            'status': company.status
            }


    def get_id(self, id: int):
        db = DataBase()
        query = self.QUERY_COMPANY_ID % id
        company = db.execute(query, many=False)
        if company:
            return {
                'id': company[0],
                'name': company[1]
                }
        

    def get_cnpj(self, cnpj: str):
        db = DataBase()
        query = self.QUERY_COMPANY_CNPJ
        company = db.execute(query, params=(cnpj,), many=False)
        if company:
            return {
                'id': company[0],
                'name': company[1],
                'cnpj': company[2], 
                'status': company[3]
                }
        return None
