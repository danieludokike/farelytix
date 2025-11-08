
import random
from datetime import datetime
from backend.app.db import SessionLocal, Base, engine
from backend.app import crud, schemas

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ts = crud.create_tracked_search(
            db,
            schemas.TrackedSearchCreate(
                origin="LGA", destination="LHR", provider="DemoProvider", passengers=1
            ),
        )
        base = 35000
        for _ in range(20):
            price = base + int(random.uniform(-2500, 2500))
            crud.add_price_snapshot(db, ts.id, price_cents=price, currency="USD", provider="DemoProvider")
        print("Seeded tracked_search ID:", ts.id)
    finally:
        db.close()

if __name__ == "__main__":
    run()
