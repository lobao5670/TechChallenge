from fastapi import APIRouter

from .endpoints import comercio, exportacao, importacao

router = APIRouter()
router.include_router(comercio.router, prefix="/comercio", tags=["Comercio"])
router.include_router(exportacao.router, prefix="/exportacao", tags=["Exportacao"])
router.include_router(importacao.router, prefix="/importacao", tags=["Importacao"])
