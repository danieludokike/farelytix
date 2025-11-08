from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import tracked_search, prices

app = FastAPI(title="Farelytix API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tracked_search.router)
app.include_router(prices.router)

@app.get("/health")
def health():
    return {"ok": True}
