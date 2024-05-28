import pandas as pd
from pandasql import sqldf


class Processamento:
    _processamento_anos_df: pd.DataFrame
    _processamento_categoria_df: pd.DataFrame
    _processamento_cultivar_df: pd.DataFrame

    @property
    def produtos(self):
        return self._processamento_cultivar_df.drop(['processamento_id'], axis=1).to_json(orient='records')

    @property
    def categorias(self):
        return self._processamento_categoria_df.drop(['processamento_id'], axis=1).to_json(orient='records')

    def produto_by_ano(self, ano):
        select_produto_by_ano = f'''
        select
            p.classificacao,
            p.categoria,
            p.produto,
            a.ano,
            a.quantidade
        from
            _processamento_cultivar_df as p

            inner join _processamento_anos_df as a 
                on a.processamento_id = p.processamento_id
        where 
            a.ano = {ano}
        '''

        return self._pysqldf(select_produto_by_ano).to_json(orient='records')

    def categoria_by_ano(self, ano):
        select_categoria_by_ano = f'''
        select
            c.classificacao,
            c.categoria,
            a.ano,
            a.quantidade
        from
            _processamento_categoria_df as c

            inner join _processamento_anos_df as a 
                on a.processamento_id = c.processamento_id
        where 
            a.ano = {ano}
        '''

        return self._pysqldf(select_categoria_by_ano).to_json(orient='records')

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_processamento()

    def _iniciar_processamento(self):
        processamento_viniferas_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
        processamento_americanas_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"
        processamento_mesa_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"
        processamento_sem_class_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"

        self._processamento_viniferas_df = pd.read_csv(processamento_viniferas_url, delimiter='\t')
        self._processamento_americanas_df = pd.read_csv(processamento_americanas_url, delimiter='\t')
        self._processamento_mesa_df = pd.read_csv(processamento_mesa_url, delimiter='\t')
        self._processamento_sem_class_df = pd.read_csv(processamento_sem_class_url, delimiter='\t')

        union_select = '''
        select 'Viníferas' as classificacao, case when control like '%!_%' escape '!' then null else cultivar end as categoria, * from _processamento_viniferas_df

        union all

        select 'Americanas e híbridas' as classificacao, case when control like '%!_%' escape '!' then null else cultivar end as categoria, * from _processamento_americanas_df

        union all

        select 'Uvas de mesa' as classificacao, case when control like '%!_%' escape '!' then null else cultivar end as categoria, * from _processamento_mesa_df

        union all

        select 'Sem classificação' as classificacao, case when control like '%!_%' escape '!' then null else cultivar end as categoria, * from _processamento_sem_class_df
        '''

        self._processamento_class_cat_df = self._pysqldf(union_select)
        self._processamento_class_cat_df['categoria'] = self._processamento_class_cat_df['categoria'].ffill()
        self._processamento_class_cat_df['processamento_id'] = self._processamento_class_cat_df.index + 1

        self._criar_processamento_categoria()
        self._criar_processamento_cultivar()
        self._criar_processamento_ano()

    def _criar_processamento_ano(self):
        # drop 2022 ->
        # Os dados disponibilizados pelo SISDEVIN no ano de 2022 estão agregados
        # [Uvas viníferas: 99.738.086; Uvas americanas ou híbridas: 565.243.922]

        self._processamento_anos_df = (
            self._processamento_class_cat_df
            .drop(
                ['id', 'classificacao', 'categoria', 'control', 'cultivar', '2022']
                , axis=1
            )
            .melt(
                id_vars=['processamento_id'],
                var_name='ano',
                value_name='quantidade'
            )
        )

    def _criar_processamento_categoria(self):
        processamento_categoria = '''
        select
          processamento_id,
          classificacao,
          categoria
        from
          _processamento_class_cat_df
        where
          control not like '%!_%' escape '!'
        '''

        self._processamento_categoria_df = self._pysqldf(processamento_categoria)

    def _criar_processamento_cultivar(self):
        processamento_cultivar = '''
        select
          processamento_id,
          classificacao,
          categoria,
          cultivar as produto
        from
          _processamento_class_cat_df
        where
          control like '%!_%' escape '!'
        '''

        self._processamento_cultivar_df = self._pysqldf(processamento_cultivar)
