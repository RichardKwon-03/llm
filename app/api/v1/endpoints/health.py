from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/health/error")
def health_error():
    raise RuntimeError("FORCED_TEST_ERROR")