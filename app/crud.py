from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_index():
    return {"message": "все работает"}
