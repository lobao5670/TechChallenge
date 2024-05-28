from fastapi import APIRouter
from app.utils.exportacao import Exportacao

router = APIRouter()
exportacao = Exportacao()


@router.get("/quantidade")
async def get_quantidade():
    """
    ### Retorna a quantidade de derivados de uva exportados.

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao da uva exportada
    - **pais**: pais da uva exportada
    - **ano**: ano referente à exportacao
    - **quantidade**: quantidade em quilos exportado
    """
    return exportacao.quantidade


@router.get("/valor")
async def get_valor():
    """
    ### Retorna a quantidade de derivados de uva exportados.

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao da uva exportada
    - **pais**: pais da uva exportada
    - **ano**: ano referente à exportacao
    - **valor**: valor em dólares exportado
    """
    return exportacao.valor
