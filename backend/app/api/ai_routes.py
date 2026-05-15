import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import ParsedEntry
from backend.app.schemas.ai import NaturalLanguageSaleRequest, ParsedSaleResponse
from backend.app.services.ai_parser import NaturalLanguageSaleParser
from backend.app.services.sales_service import create_sale_from_parsed

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.post("/parse-sale", response_model=ParsedSaleResponse)
def parse_sale(payload: NaturalLanguageSaleRequest, db: Session = Depends(get_db)):
    parser = NaturalLanguageSaleParser()
    parsed = parser.parse(payload.text)

    entry = ParsedEntry(
        raw_text=payload.text,
        parsed_json=json.dumps(parsed.model_dump(), ensure_ascii=False),
        was_saved_as_sale=False,
    )
    db.add(entry)
    db.commit()

    if payload.save_as_sale:
        create_sale_from_parsed(db, parsed)
        entry.was_saved_as_sale = True
        db.commit()

    return parsed
