from fastapi import APIRouter
from app.utils.comercio import Comercio

router = APIRouter()
comercio = Comercio()


@router.get("/produtos")
async def get_produtos():
    """
    ### Retorna todos os produtos e suas categorias.

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria do produto comercializado
    - **produto**: produto comercializado
    """
    return comercio.produtos


@router.get("/categorias")
async def get_categorias():
    """
    ### Retorna todas as categorias comercializadas.

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria do produto comercializado
    """
    return comercio.categorias


@router.get("/produto/{ano}")
async def get_produto_by_ano(ano: int):
    """
    ### Retorna a quantidade comercializada do produto referente ao ano.

    Paramêtros:
    - **ano**: ano do produto comercializado

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria do produto comercializado
    - **produto**: produto comercializado
    - **ano**: ano do produto comercializado
    - **quantidade**: quantidade em litros comercializada
    """
    return comercio.produto_by_ano(ano)


@router.get("/categoria/{ano}")
async def get_categoria_by_ano(ano: int):
    """
    ### Retorna a quantidade comercializada da categoria referente ao ano.

    Paramêtros:
    - **ano**: ano da categoria comercializado

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria comercializada
    - **ano**: ano da categoria comercializado
    - **quantidade**: quantidade em litros comercializada
    """
    return comercio.categoria_by_ano(ano)
