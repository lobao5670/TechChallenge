from fastapi import APIRouter
from app.utils.importacao import Importacao

router = APIRouter()
importacao = Importacao()


@router.get("/quantidade")
async def get_quantidade():
    """
    ### Retorna a quantidade de derivados de uva importados.

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao da uva importada
    - **pais**: pais da uva importada
    - **ano**: ano referente à importacao
    - **quantidade**: quantidade em quilos importado
    """
    return importacao.quantidade


@router.get("/valor")
async def get_valor():
    """
    ### Retorna a quantidade de derivados de uva importados.

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao da uva importada
    - **pais**: pais da uva importada
    - **ano**: ano referente à importacao
    - **valor**: valor em dólares importado
    """
    return importacao.valor
