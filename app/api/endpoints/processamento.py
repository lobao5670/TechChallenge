from fastapi import APIRouter
from app.utils.processamento import Processamento

router = APIRouter()
processamento = Processamento()


@router.get("/produtos")
async def get_produtos():
    return processamento.produtos


@router.get("/categorias")
async def get_categorias():
    return processamento.categorias


@router.get("/anos")
async def get_anos():
    return processamento.anos
