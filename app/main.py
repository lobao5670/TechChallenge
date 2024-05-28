from fastapi import FastAPI
from app.api.api import router as api_router

description = """
Essa API apresenta informações provindas do banco de dados de uva, vinhos e derivados do Estado do Rio Grande do Sul, fornecidos pela Embrapa. Tais informações são referentes à:
* Produção
* Processamento
* Comercialização
* Importação
* Exportação

Mais informações em [Banco de dados de uva, vinho e derivados](http://vitibrasil.cnpuv.embrapa.br/index.php).
"""

app = FastAPI(
    title="Vitivinicultura API",
    description=description
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api")
