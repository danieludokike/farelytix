from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas
from ..services.forecast import simple_forecast

router = APIRouter(prefix="/api/prices", tags=["prices"])

@router.get("/{tracked_id}", response_model=schemas.PriceSeriesResponse)
def get_price_series(tracked_id: str, db: Session = Depends(get_db)):
    search = crud.get_tracked_search(db, tracked_id)
    if not search:
        raise HTTPException(status_code=404, detail="Tracked search not found")

    snaps = crud.get_snapshots_for_search(db, tracked_id, limit=500)
    series = [{"ds": s.scraped_at, "price": s.price_cents / 100.0} for s in snaps]

    forecast = simple_forecast(series, horizon=7) if series else []

    return {
        "id": tracked_id,
        "currency": snaps[0].currency if snaps else "USD",
        "series": series,
        "forecast": forecast
    }

@router.post("/dev/random-snapshot/{tracked_id}")
def add_random_snapshot(tracked_id: str, db: Session = Depends(get_db)):
    search = crud.get_tracked_search(db, tracked_id)
    if not search:
        raise HTTPException(status_code=404, detail="Tracked search not found")

    import random
    price_cents = random.randint(25000, 60000)
    crud.add_price_snapshot(db, tracked_id=tracked_id, price_cents=price_cents,
                            currency="USD", provider=search.provider or "DevProvider")
    return {"ok": True, "new_price": price_cents / 100.0}
