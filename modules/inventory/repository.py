from fastapi import HTTPException, status
from psycopg2 import IntegrityError

from core.db import DataBase
from modules.inventory.schemas import InventoryCreate


class InventoryRepository:
    QUERY_INVENTORY = '''
    SELECT
        iv.id,
        iv.product_id,
        pr.name,
        iv.quantity,
        iv.update_date
    FROM inventory iv
    JOIN product pr ON iv.product_id = pr.id;
    '''
    QUERY_INVENTORY_ID = '''
    SELECT
        iv.id,
        iv.product_id,
        pr.name,
        iv.quantity,
        iv.update_date
    FROM inventory iv
    JOIN product pr ON iv.product_id = pr.id
    WHERE iv.id = %s;
    '''
    QUERY_CREATE_INVENTORY = 'INSERT INTO inventory (product_id, quantity) VALUES (%s, %s) RETURNING id, update_date;'


    def get_all(self):
        db = DataBase()
        query = self.QUERY_INVENTORY
        inventories = db.execute(query)
        results = []
        for inventory in inventories:
            results.append({
                'id': inventory[0],
                'product_id': inventory[1],
                'product': {
                    'name': inventory[2]
                },
                'quantity': inventory[3],
                'update_date': inventory[4].date()
            })
        return results
    

    def get_id(self, id:int):
        db = DataBase()
        query = self.QUERY_INVENTORY_ID % id
        inventory = db.execute(query, many=False)
        if inventory:
            return {
                'id': inventory[0],
                'product_id': inventory[1],
                'product': {
                    'name': inventory[2]
                },
                'quantity': inventory[3],
                'update_date': inventory[4].date()
            }
        
    
    def save(self, inventory:InventoryCreate):
        db = DataBase()
        query = self.QUERY_CREATE_INVENTORY
        params = (inventory.product_id, inventory.quantity)

        result = db.commit(query, params)

        return {
            'id': result[0],
            'product_id': inventory.product_id,
            'quantity': inventory.quantity,
            'update_date': result[1].date()
        }
