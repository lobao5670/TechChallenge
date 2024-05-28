from fastapi import APIRouter

from .endpoints import comercio, exportacao, importacao, processamento, producao

router = APIRouter()
router.include_router(comercio.router, prefix="/comercio", tags=["Comercio"])
router.include_router(exportacao.router, prefix="/exportacao", tags=["Exportacao"])
router.include_router(importacao.router, prefix="/importacao", tags=["Importacao"])
router.include_router(processamento.router, prefix="/processamento", tags=["Processamento"])
router.include_router(producao.router, prefix="/producao", tags=["Producao"])
