from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.reports import DashboardSummary
from backend.app.services.report_service import dashboard_summary, generate_arabic_daily_report

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/dashboard", response_model=DashboardSummary)
def dashboard(db: Session = Depends(get_db)):
    return dashboard_summary(db)


@router.get("/daily-arabic")
def daily_arabic(db: Session = Depends(get_db)):
    return {"report": generate_arabic_daily_report(db)}
