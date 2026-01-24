from fastapi import APIRouter, Depends

from src.core.auth import get_current_user

router = APIRouter()


@router.get("/me")
def read_profile(user: str = Depends(get_current_user)) -> dict:
    return {"user": user}
