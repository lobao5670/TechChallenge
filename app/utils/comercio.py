import pandas as pd
from pandasql import sqldf


class Comercio:
    _comercio_produtos_df: pd.DataFrame
    _comercio_categorias_df: pd.DataFrame
    _comercio_anos_df: pd.DataFrame

    @property
    def produtos(self):
        return self._comercio_produtos_df.drop(['id'], axis=1).to_json(orient='records')

    @property
    def categorias(self):
        return self._comercio_categorias_df.drop(['id'], axis=1).to_json(orient='records')

    def produto_by_ano(self, ano):
        select_produto_by_ano = f'''
        select
            p.categoria,
            p.produto,
            a.ano,
            a.quantidade
        from
            _comercio_produtos_df as p

            inner join _comercio_anos_df as a 
                on a.id = p.id
        where 
            a.ano = {ano}
        '''

        return self._pysqldf(select_produto_by_ano).to_json(orient='records')

    def categoria_by_ano(self, ano):
        select_categoria_by_ano = f'''
        select
            c.categoria,
            a.ano,
            a.quantidade
        from
            _comercio_categorias_df as c

            inner join _comercio_anos_df as a 
                on a.id = c.id
        where 
            a.ano = {ano}
        '''

        return self._pysqldf(select_categoria_by_ano).to_json(orient='records')

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_comercio()

    def _iniciar_comercio(self):
        comercializacao_url = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
        self._comercializacao_df = pd.read_csv(comercializacao_url, delimiter=';')

        add_categoria = '''
        select
          case 
            when ifnull(control, produto) = produto then produto
            else null
          end as categoria,
          *
        from
          _comercializacao_df
        '''

        self._comercio_add_categoria_df = self._pysqldf(add_categoria)
        self._comercio_add_categoria_df['categoria'] = self._comercio_add_categoria_df['categoria'].ffill()

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
          _comercio_add_categoria_df
        where
          control <> produto
        '''

        self._comercio_produtos_df = self._pysqldf(comercio_produto)

    def _criar_comercio_categoria(self):
        comercio_categorias = '''
        select
          id,
          categoria
        from
          _comercio_add_categoria_df
        where
          ifnull(control, produto) = produto
        '''

        self._comercio_categorias_df = self._pysqldf(comercio_categorias)

    def _criar_comercio_ano(self):
        self._comercio_anos_df = (
            self._comercializacao_df
            .drop(['control', 'Produto'], axis=1)
            .melt(
                id_vars=['id'],
                var_name='ano',
                value_name='quantidade')
        )
