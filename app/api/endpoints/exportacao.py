from fastapi import APIRouter
from app.utils.exportacao import Exportacao

router = APIRouter()
exportacao = Exportacao()


@router.get("/quantidade")
async def get_quantidade():
    return exportacao.quantidade


@router.get("/valor")
async def get_valor():
    return exportacao.valor
