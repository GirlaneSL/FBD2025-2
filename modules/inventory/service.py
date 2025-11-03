from fastapi import HTTPException, status
from psycopg2 import IntegrityError

from modules.inventory.repository import InventoryRepository
from modules.inventory.schemas import InventoryCreate


class InventoryService:
    def get_inventories(self):
        repository = InventoryRepository()
        inventories = repository.get_all()
        
        if not inventories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não há estoques cadastrados!'
            )

        return inventories
    

    def get_inventory_id(self, id:int):
        repository = InventoryRepository()
        inventory = repository.get_id(id)

        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Estoque com id {id} não existe!'
            )

        return inventory


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
