from pydantic import BaseModel, Field


class TypeProduct(BaseModel):
    id: int
    name: str


class TypeProductCreate(BaseModel):
    name: str
    cod_type: str = Field(..., example='XX-000')
    company_id: int
