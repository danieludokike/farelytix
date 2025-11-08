
from sqlalchemy import (
    Column, String, Date, DateTime, Integer, BigInteger,
    ForeignKey, func, JSON, Text
)
from sqlalchemy.orm import relationship
from .db import Base
import uuid

def _uuid(): return str(uuid.uuid4())

class TrackedSearch(Base):
    __tablename__ = "tracked_search"
    id = Column(String, primary_key=True, default=_uuid)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    depart_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    provider = Column(String, nullable=True)
    passengers = Column(Integer, default=1)
    cabin_class = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    snapshots = relationship(
        "PriceSnapshot", back_populates="search", cascade="all, delete-orphan"
    )

class PriceSnapshot(Base):
    __tablename__ = "price_snapshot"
    id = Column(String, primary_key=True, default=_uuid)
    tracked_search_id = Column(
        String, ForeignKey("tracked_search.id", ondelete="CASCADE"), index=True
    )
    provider = Column(String, nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    currency = Column(String(3), default="USD")
    price_cents = Column(BigInteger, nullable=False)
    flights_json = Column(JSON, nullable=True)
    raw_html_path = Column(Text, nullable=True)

    search = relationship("TrackedSearch", back_populates="snapshots")
