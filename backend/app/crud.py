
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from . import models, schemas

def create_tracked_search(db: Session, data: schemas.TrackedSearchCreate):
    obj = models.TrackedSearch(
        origin=data.origin.upper(),
        destination=data.destination.upper(),
        depart_date=data.depart_date,
        return_date=data.return_date,
        provider=data.provider,
        passengers=data.passengers,
        cabin_class=data.cabin_class,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_tracked_searches(db: Session):
    stmt = select(models.TrackedSearch).order_by(models.TrackedSearch.created_at.desc())
    return db.scalars(stmt).all()

def get_tracked_search(db: Session, tracked_id: str):
    return db.get(models.TrackedSearch, tracked_id)

def add_price_snapshot(db: Session, tracked_id: str, price_cents: int,
                       currency: str = "USD", flights_json=None, provider: str | None = None):
    snap = models.PriceSnapshot(
        tracked_search_id=tracked_id,
        provider=provider,
        price_cents=price_cents,
        currency=currency,
        scraped_at=datetime.now(timezone.utc),
        flights_json=flights_json,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap

def get_snapshots_for_search(db: Session, tracked_id: str, limit: int = 500):
    stmt = (
        select(models.PriceSnapshot)
        .where(models.PriceSnapshot.tracked_search_id == tracked_id)
        .order_by(models.PriceSnapshot.scraped_at.asc())
        .limit(limit)
    )
    return db.scalars(stmt).all()
