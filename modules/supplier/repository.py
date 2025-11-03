from core.db import DataBase
from modules.supplier.schemas import SupplierCreate


class SupplierRepository:
    QUERY_SUPPLIER = 'SELECT id, name, cnpj, status, company_id FROM supplier'
    QUERY_SUPPLIER_ID = 'SELECT id, name, cnpj, status, company_id FROM supplier WHERE id = %s'
    QUERY_CREATE_SUPPLIER = 'INSERT INTO supplier (name, cnpj, status, company_id) VALUES (%s, %s, %s, %s) RETURNING id'
    QUERY_SUPPLIER_CNPJ = 'SELECT id, name, cnpj, status, company_id FROM supplier WHERE cnpj = %s;'


    def get_all(self):
        db = DataBase()
        suppliers = db.execute(self.QUERY_SUPPLIER)
        results = []
        for supplier in suppliers:
            results.append({
                'id': supplier[0],
                'name': supplier[1],
                'cnpj': supplier[2],
                'status': supplier[3],
                'company_id': supplier[4]
                })
        return results
    

    def get_id(self, id:int):
        db = DataBase()
        query = self.QUERY_SUPPLIER_ID % id
        supplier = db.execute(query, many=False)
        if supplier:
            return {
                'id': supplier[0],
                'name': supplier[1],
                'cnpj': supplier[2],
                'status': supplier[3],
                'company_id': supplier[4]
                }


    def save(self, supplier:SupplierCreate):
        db = DataBase()
        query = self.QUERY_CREATE_SUPPLIER
        params = (supplier.name, supplier.cnpj, supplier.status, supplier.company_id)
        result = db.commit(query, params)
        return {
            'id': result[0],
            'name': supplier.name,
            'cnpj': supplier.cnpj,
            'status': supplier.status,
            'company_id': supplier.company_id
            }
    

    def get_cnpj(self, cnpj: str):
        db = DataBase()
        query = self.QUERY_SUPPLIER_CNPJ
        supplier = db.execute(query, params=(cnpj,), many=False)
        if supplier:
            return {
                'id': supplier[0],
                'name': supplier[1],
                'cnpj': supplier[2],
                'status': supplier[3],
                'company_id': supplier[4]
                }
        return None
    