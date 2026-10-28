from fastapi import APIRouter 

router = APIRouter()

@router.get("/health")
async def health_check():
    return{"status": "System is Healthy, V.1.0"}