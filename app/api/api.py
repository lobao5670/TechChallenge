from fastapi import APIRouter

from .endpoints import comercio, exportacao, importacao, processamento, producao

router = APIRouter()
router.include_router(comercio.router, prefix="/comercio", tags=["comercio"])
router.include_router(exportacao.router, prefix="/exportacao", tags=["exportacao"])
router.include_router(importacao.router, prefix="/importacao", tags=["importacao"])
router.include_router(processamento.router, prefix="/processamento", tags=["processamento"])
router.include_router(producao.router, prefix="/producao", tags=["producao"])
