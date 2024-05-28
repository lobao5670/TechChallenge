from fastapi import APIRouter
from app.utils.processamento import Processamento

router = APIRouter()
processamento = Processamento()


@router.get("/produtos")
async def get_produtos():
    """
    ### Retorna todos os produtos, suas categorias e suas classificações.

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao do produto processado
    - **categoria**: categoria do produto processado
    - **produto**: produto processado
    """
    return processamento.produtos


@router.get("/categorias")
async def get_categorias():
    """
    ### Retorna todas as categorias e classificações processadas.

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao do produto processado
    - **categoria**: categoria do produto processado
    """
    return processamento.categorias


@router.get("/processamento/{ano}")
async def get_produto_by_ano(ano: int):
    """
    ### Retorna a quantidade processada do produto referente ao ano.

    Paramêtros:
    - **ano**: ano do produto processado

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao do produto processado
    - **categoria**: categoria do produto processado
    - **produto**: produto processado
    - **ano**: ano do produto processado
    - **quantidade**: quantidade em quilos processada
    """
    return processamento.produto_by_ano(ano)


@router.get("/categoria/{ano}")
async def get_categoria_by_ano(ano: int):
    """
    ### Retorna a quantidade processada da categoria referente ao ano.

    Paramêtros:
    - **ano**: ano da categoria processada

    Retorna um Dataframe formatado em JSON com:
    - **classificacao**: classificacao do produto processado
    - **categoria**: categoria processada
    - **ano**: ano da categoria processada
    - **quantidade**: quantidade em quilos processada
    """
    return processamento.categoria_by_ano(ano)
