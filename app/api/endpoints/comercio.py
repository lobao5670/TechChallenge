from fastapi import APIRouter
from app.utils.comercio import Comercio

router = APIRouter()
comercio = Comercio()


@router.get("/produtos")
async def get_produtos():
    return comercio.produtos


@router.get("/categorias")
async def get_categorias():
    return comercio.categorias


@router.get("/anos")
async def get_anos():
    return comercio.anos
