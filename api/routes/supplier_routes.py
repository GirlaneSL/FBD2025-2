from typing import Optional
from fastapi import APIRouter

from modules.supplier import schemas
from modules.supplier.service import SupplierService

router = APIRouter(prefix='/fornecedor', tags=['Supplier'])


@router.get('/', response_model=list[schemas.Supplier])
def list_suppliers():
    service = SupplierService()
    return service.get_suppliers()


@router.get('/{id}', response_model=Optional[schemas.Supplier])
def get_supplier_by_id(id:int):
    service = SupplierService()
    return service.get_supplier_id(id)


@router.post('/', response_model=schemas.Supplier)
def add_supplier(supplier:schemas.SupplierCreate):
    service = SupplierService()
    return service.create_supplier(supplier)
