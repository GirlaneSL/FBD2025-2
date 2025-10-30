from fastapi import FastAPI
from api.routes import company_routes, type_product_routes, supplier_routes, product_routes, inventory_routes

app = FastAPI()
app.include_router(company_routes.router)
app.include_router(type_product_routes.router)
app.include_router(supplier_routes.router)
app.include_router(product_routes.router)
app.include_router(inventory_routes.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
