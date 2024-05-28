from fastapi import APIRouter

from .endpoints import comercio

router = APIRouter()
router.include_router(comercio.router, prefix="/comercio", tags=["Comercio"])
