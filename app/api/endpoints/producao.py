from fastapi import APIRouter
from app.utils.producao import Producao

router = APIRouter()
producao = Producao()


@router.get("/produtos")
async def get_produtos():
    """
    ### Retorna todos os produtos e suas categorias.

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria do produto produzido
    - **produto**: produto produzido
    """
    return producao.produtos


@router.get("/categorias")
async def get_categorias():
    """
    ### Retorna todas as categorias produzidas.

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria do produto produzido
    """
    return producao.categorias


@router.get("/produto/{ano}")
async def get_produto_by_ano(ano: int):
    """
    ### Retorna a quantidade produzida do produto referente ao ano.

    Paramêtros:
    - **ano**: ano do produto produzido

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria do produto produzido
    - **produto**: produto produzido
    - **ano**: ano do produto produzido
    - **quantidade**: quantidade em litros produzida
    """
    return producao.produto_by_ano(ano)


@router.get("/categoria/{ano}")
async def get_categoria_by_ano(ano: int):
    """
    ### Retorna a quantidade produzida da categoria referente ao ano.

    Paramêtros:
    - **ano**: ano da categoria produzido

    Retorna um Dataframe formatado em JSON com:
    - **categoria**: categoria produzida
    - **ano**: ano da categoria produzido
    - **quantidade**: quantidade em litros produzida
    """
    return producao.categoria_by_ano(ano)
