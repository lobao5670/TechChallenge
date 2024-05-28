from fastapi import APIRouter
from app.utils.importacao import Importacao

router = APIRouter()
importacao = Importacao()


@router.get("/quantidade")
async def get_quantidade():
    return importacao.quantidade


@router.get("/valor")
async def get_valor():
    return importacao.valor
