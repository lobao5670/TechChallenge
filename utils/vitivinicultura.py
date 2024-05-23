from utils.comercio import Comercio
from utils.importacao import Importacao
from utils.processamento import Processamento
from utils.producao import Producao


class Vitivinicultura:

    def __init__(self):
        self.producao = Producao()
        self.processamento = Processamento()
        self.comercio = Comercio()
        self.importacao = Importacao()