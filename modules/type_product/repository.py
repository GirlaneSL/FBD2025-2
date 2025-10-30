from core.db import DataBase
from modules.type_product.schemas import TypeProductCreate


class TypeProductRepostiroy:
    QUERY_TYPE_PRODUCTS = 'SELECT id, name, cod, company_id FROM type_product'
    QUERY_TYPE_PRODUCT_ID = 'SELECT id, name, cod, company_id FROM type_product WHERE id = %s'
    QUERY_CREATE_TYPE_PRODUCT = 'INSERT INTO type_product (name, cod, company_id) VALUES (%s, %s, %s) RETURNING id'
    QUERY_TYPE_PRODUCTS_COD = 'SELECT id, name, cod, company_id FROM type_product WHERE cod = %s;'
    

    def get_all(self):
        db = DataBase()
        type_products = db.execute(self.QUERY_TYPE_PRODUCTS)
        results = []
        for type_product in type_products:
            results.append({'id': type_product[0], 'name': type_product[1], 'cod': type_product[2], 'company_id': type_product[3]})
        return results
    

    def get_id(self, id:int):
        db = DataBase()
        query = self.QUERY_TYPE_PRODUCT_ID % id
        type_product = db.execute(query, many=False)
        if type_product:
            return {'id': type_product[0], 'name': type_product[1], 'cod': type_product[2], 'company_id': type_product[3]}
        

    def save(self, type_product:TypeProductCreate):
        db = DataBase()
        query = self.QUERY_CREATE_TYPE_PRODUCT
        params = (type_product.name, type_product.cod_type, type_product.company_id)
        result = db.commit(query, params)
        return {'id': result[0], 'name': type_product.name, 'cod': type_product.cod_type, 'company_id': type_product.company_id}
    

    def get_cod(self, cod:str):
        db = DataBase()
        query = self.QUERY_TYPE_PRODUCTS_COD
        type_product = db.execute(query, params=(cod,), many=False)
        if type_product:
            return {'id': type_product[0], 'name': type_product[1], 'cod': type_product[2], 'company_id': type_product[3]}
        return None
