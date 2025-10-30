from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints


class Supplier(BaseModel):
    id: int
    name: str
    cnpj: str
    status: str
    company_id: int


class SupplierCreate(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=255)]
    cnpj: str = Field(..., example="00.000.000/0000-00")
    status: str = "ATIVO"
    company_id: int


class SupplierResponse(BaseModel):
    id: int
    name: str
