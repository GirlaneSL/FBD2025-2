from core.db import DataBase
from modules.product.schemas import ProductCreate


class ProductRepository:
    QUERY_PRODUCT = '''
    SELECT 
        pr.id,
        pr.name,
        pr.description,
        pr.price,
        tp.id AS type_id,
        tp.name AS type_name,
        sp.id AS supplier_id,
        sp.name AS supplier_name,
        pr.company_id
    FROM product pr
    JOIN type_product tp ON pr.type_product_id = tp.id
    JOIN supplier sp ON pr.supplier_id = sp.id
    '''
    QUERY_PRODUCT_ID = '''SELECT 
        pr.id,
        pr.name,
        pr.description,
        pr.price,
        tp.id AS type_id,
        tp.name AS type_name,
        sp.id AS supplier_id,
        sp.name AS supplier_name,
        pr.company_id
    FROM product pr
    JOIN type_product tp ON pr.type_product_id = tp.id
    JOIN supplier sp ON pr.supplier_id = sp.id
    WHERE pr.id = %s'''
    QUERY_CREATE_PRODUCT = 'INSERT INTO product (name, description, price, type_product_id, supplier_id, company_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id'
    QUERY_PRODUCTS_SUPPLIER_AND_TYPE = '''
    SELECT 
        pr.id,
        pr.name,
        pr.description,
        pr.price,
        tp.id AS type_id,
        tp.name AS type_name,
        sp.id AS supplier_id,
        sp.name AS supplier_name,
        pr.company_id
    FROM product pr
    JOIN type_product tp ON pr.type_product_id = tp.id
    JOIN supplier sp ON pr.supplier_id = sp.id
    WHERE pr.company_id = %s
    '''


    def get_all(self):
        db = DataBase()
        products = db.execute(self.QUERY_PRODUCT)
        results = []
        for product in products:
            results.append({
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': float(product[3]),
                'type': {
                    'id': product[4],
                    'name': product[5]
                },
                'supplier': {
                    'id': product[6],
                    'name': product[7]
                },
                'company_id': product[8]
            })

        return results
        

    def get_id(self, id:int):
        db = DataBase()
        query = self.QUERY_PRODUCT_ID % id
        product = db.execute(query, many=False)
        if product:
            return {
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': float(product[3]),
                'type': {
                    'id': product[4],
                    'name': product[5]
                },
                'supplier': {
                    'id': product[6],
                    'name': product[7]
                },
                'company_id': product[8]
                }
        

    def save(self, product:ProductCreate):
        db = DataBase()
        query = self.QUERY_CREATE_PRODUCT
        params = (product.name, product.description, product.price, product.type_id, product.supplier_id, product.company_id)
        result = db.commit(query, params)
        return {
            'id': result[0],
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'type_id': product.type_id,
            'supplier_id': product.supplier_id,
            'company_id': product.company_id
            }


    def get_company_products(self, company_id: int):
        db = DataBase()
        query = self.QUERY_PRODUCTS_SUPPLIER_AND_TYPE % company_id
        products = db.execute(query)
        
        results = []
        for product in products:
            results.append({
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'price': float(product[3]),
                'type': {
                    'id': product[4],
                    'name': product[5]
                },
                'supplier': {
                    'id': product[6],
                    'name': product[7]
                },
                'company_id': product[8]
            })
        
        return results
