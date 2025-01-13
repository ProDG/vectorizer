from fastapi import FastAPI

from app.api.routers.vectorize_routers import vectorize_router


app = FastAPI()
app.include_router(vectorize_router, prefix='/api/vectorize', tags=['Vectorize'])
