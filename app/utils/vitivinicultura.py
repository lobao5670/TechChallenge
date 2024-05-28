from app.utils.comercio import Comercio
from app.utils.exportacao import Exportacao
from app.utils.importacao import Importacao
from app.utils.processamento import Processamento
from app.utils.producao import Producao


class Vitivinicultura:
    producao: Producao
    processamento: Processamento
    comercio: Comercio
    importacao: Importacao
    exportacao: Exportacao

    def __init__(self):
        self.producao = Producao()
        self.processamento = Processamento()
        self.comercio = Comercio()
        self.importacao = Importacao()
        self.exportacao = Exportacao()
