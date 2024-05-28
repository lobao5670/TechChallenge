from fastapi import APIRouter
from app.utils.producao import Producao

router = APIRouter()
producao = Producao()


@router.get("/produtos")
async def get_produtos():
    return producao.produtos


@router.get("/categorias")
async def get_categorias():
    return producao.categorias


@router.get("/anos")
async def get_anos():
    return producao.anos
