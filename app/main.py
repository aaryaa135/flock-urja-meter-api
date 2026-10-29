from fastapi import FastAPI

from app.api.meters import router as meters_router
from app.api.transformers import router as transformers_router

app = FastAPI(title="Flock Energy Urja Meter API")


@app.get("/health")
def health():
    """Check application health only. Does not check portal connectivity."""
    return {"status": "ok"}


app.include_router(meters_router)
app.include_router(transformers_router)
