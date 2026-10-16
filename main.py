import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

# ====== CHANGE THIS to your exact logged-in email ======
EMAIL = "your-email@example.com"
# =======================================================

ALLOWED_ORIGIN = "https://dash-470s77.example.com"

app = FastAPI()


# --- Middleware #1: add X-Request-ID and X-Process-Time to EVERY response ---
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


# --- Middleware #2: CORS (added AFTER, so it wraps the one above) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],   # ONLY this origin, no "*"
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/stats")
def stats(values: str = ""):
    try:
        nums = [int(v) for v in values.split(",") if v.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    if not nums:
        raise HTTPException(status_code=400, detail="provide at least one value")

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
