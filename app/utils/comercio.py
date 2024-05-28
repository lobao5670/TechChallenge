import pandas as pd
from pandasql import sqldf


class Comercio:
    comercio_produtos_df: pd.DataFrame
    comercio_categorias_df: pd.DataFrame
    comercio_anos_df: pd.DataFrame

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_comercio()

    def _iniciar_comercio(self):
        comercializacao_url = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
        self.comercializacao_df = pd.read_csv(comercializacao_url, delimiter=';')

        add_categoria = '''
        select
          case 
            when ifnull(control, produto) = produto then produto
            else null
          end as categoria,
          *
        from
          comercializacao_df
        '''

        self.comercio_add_categoria_df = self._pysqldf(add_categoria)
        self.comercio_add_categoria_df['categoria'] = self.comercio_add_categoria_df['categoria'].ffill()

        self._criar_comercio_categoria()
        self._criar_comercio_produto()
        self._criar_comercio_ano()

    def _criar_comercio_produto(self):
        comercio_produto = '''
        select
          id,
          categoria,
          produto
        from
          comercio_add_categoria_df
        where
          control <> produto
        '''

        self.comercio_produtos_df = self._pysqldf(comercio_produto)

    def _criar_comercio_categoria(self):
        comercio_categorias = '''
        select
          id,
          categoria
        from
          comercio_add_categoria_df
        where
          ifnull(control, produto) = produto
        '''

        self.comercio_categorias_df = self._pysqldf(comercio_categorias)

    def _criar_comercio_ano(self):
        self.comercio_anos_df = (
            self.comercializacao_df
            .drop(['control', 'Produto'], axis=1)
            .melt(
                id_vars=['id'],
                var_name='ano',
                value_name='quantidade')
        )
