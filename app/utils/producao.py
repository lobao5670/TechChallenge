import pandas as pd
from pandasql import sqldf


class Producao:
    producao_produtos_df: pd.DataFrame
    producao_categorias_df: pd.DataFrame
    producao_anos_df: pd.DataFrame

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_producao()

    def _iniciar_producao(self):
        producao_url = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
        self.producao_df = pd.read_csv(producao_url, delimiter=';')

        add_categoria = '''
        select
          nullif(substr(control, 1, instr(control, '_') - 1), '') as categoria,
          *
        from
          producao_df
        '''

        self.producao_add_categoria_df = self._pysqldf(add_categoria).bfill()

        self._criar_producao_categoria()
        self._criar_producao_produto()
        self._criar_producao_ano()

    def _criar_producao_produto(self):
        producao_produto = '''
        select
          id,
          categoria,
          produto
        from
          producao_add_categoria_df
        where
          control <> produto
        '''

        self.producao_produtos_df = self._pysqldf(producao_produto)

    def _criar_producao_categoria(self):
        producao_categorias = '''
        select
          id,
          categoria,
          produto
        from
          producao_add_categoria_df
        where
          control = produto
        '''

        self.producao_categorias_df = self._pysqldf(producao_categorias)

    def _criar_producao_ano(self):
        self.producao_anos_df = (
            self.producao_df
            .drop(['control', 'produto'], axis=1)
            .melt(
                id_vars=['id'],
                var_name='ano',
                value_name='quantidade')
        )