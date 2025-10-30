from typing import Optional
from fastapi import APIRouter

from modules.inventory import schemas
from modules.inventory.service import InventoryService

router = APIRouter(prefix='/inventory', tags=['Inventory'])

@router.get('/', response_model=list[schemas.InventotyResponse])
def list_inventories():
    service = InventoryService()
    return service.get_inventories()


@router.get('{id}', response_model=Optional[schemas.InventotyResponse])
def get_product_by_id(id:int):
    service = InventoryService()
    return service.get_inventory_id(id)


@router.post('/', response_model=schemas.Inventory)
def add_inventory(inventory:schemas.InventoryCreate):
    service = InventoryService()
    return service.create_inventory(inventory)
