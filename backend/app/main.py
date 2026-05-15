from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.ai_routes import router as ai_router
from backend.app.api.customers_routes import router as customers_router
from backend.app.api.products_routes import router as products_router
from backend.app.api.reports_routes import router as reports_router
from backend.app.api.sales_routes import router as sales_router
from backend.app.core.config import settings
from backend.app.db.database import init_db

app = FastAPI(
    title=settings.app_name,
    description="AI-powered Arabic business ledger for Yemeni small shops.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "running",
        "docs": "/docs",
    }


app.include_router(customers_router)
app.include_router(products_router)
app.include_router(sales_router)
app.include_router(ai_router)
app.include_router(reports_router)
