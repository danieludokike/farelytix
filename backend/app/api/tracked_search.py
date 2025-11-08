from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db, Base, engine
from .. import schemas, crud

router = APIRouter(prefix="/api/tracked-search", tags=["tracked-search"])

# MVP convenience: create tables on first import
Base.metadata.create_all(bind=engine)

@router.post("", response_model=schemas.TrackedSearchOut)
def create_tracked(item: schemas.TrackedSearchCreate, db: Session = Depends(get_db)):
    return crud.create_tracked_search(db, item)

@router.get("", response_model=list[schemas.TrackedSearchOut])
def list_tracked(db: Session = Depends(get_db)):
    return crud.list_tracked_searches(db)

@router.get("/{tracked_id}", response_model=schemas.TrackedSearchOut)
def get_tracked(tracked_id: str, db: Session = Depends(get_db)):
    obj = crud.get_tracked_search(db, tracked_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tracked search not found")
    return obj
