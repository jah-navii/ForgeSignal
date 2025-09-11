from fastapi import FastAPI
from app.routes import ingestion_router

app = FastAPI(title="Fear & Greed Sentiment Engine")

app.include_router(ingestion_router.router)
