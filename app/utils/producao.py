import pandas as pd
from pandasql import sqldf


class Producao:
    _producao_produtos_df: pd.DataFrame
    _producao_categorias_df: pd.DataFrame
    _producao_anos_df: pd.DataFrame

    @property
    def produtos(self):
        return self._producao_produtos_df.to_json(orient='records')

    @property
    def categorias(self):
        return self._producao_categorias_df.to_json(orient='records')

    @property
    def anos(self):
        return self._producao_anos_df.to_json(orient='records')

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_producao()

    def _iniciar_producao(self):
        producao_url = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
        self._producao_df = pd.read_csv(producao_url, delimiter=';')

        add_categoria = '''
        select
          case 
            when ifnull(control, produto) = produto then produto
            else null
          end as categoria,
          *
        from
          _producao_df
        '''

        self._producao_add_categoria_df = self._pysqldf(add_categoria)
        self._producao_add_categoria_df['categoria'] = self._producao_add_categoria_df['categoria'].ffill()

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
          _producao_add_categoria_df
        where
          control <> produto
        '''

        self._producao_produtos_df = self._pysqldf(producao_produto)

    def _criar_producao_categoria(self):
        producao_categorias = '''
        select
          id,
          categoria,
          produto
        from
          _producao_add_categoria_df
        where
          ifnull(control, produto) = produto
        '''

        self._producao_categorias_df = self._pysqldf(producao_categorias)

    def _criar_producao_ano(self):
        self._producao_anos_df = (
            self._producao_df
            .drop(['control', 'produto'], axis=1)
            .melt(
                id_vars=['id'],
                var_name='ano',
                value_name='quantidade')
        )
