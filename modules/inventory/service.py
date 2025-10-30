from fastapi import HTTPException, status
from psycopg2 import IntegrityError

from modules.inventory.repository import InventoryRepository
from modules.inventory.schemas import InventoryCreate


class InventoryService:
    def get_inventories(self):
        repository = InventoryRepository()
        return repository.get_all()
    

    def get_inventory_id(self, id:int):
        repository = InventoryRepository()
        return repository.get_id(id)


    def create_inventory(self, inventory:InventoryCreate):
        repository = InventoryRepository()

        try:
            return repository.save(inventory)
        except IntegrityError as e:
            if 'fk_inventory_product' in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Produto com id {inventory.product_id} não existe!'
                )
