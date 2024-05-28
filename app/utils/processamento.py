import pandas as pd
from pandasql import sqldf


class Processamento:

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_processamento()

    def _iniciar_processamento(self):
        processamento_viniferas_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
        processamento_americanas_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"
        processamento_mesa_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"
        processamento_sem_class_url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"

        self.processamento_viniferas_df = pd.read_csv(processamento_viniferas_url, delimiter='\t')
        self.processamento_americanas_df = pd.read_csv(processamento_americanas_url, delimiter='\t')
        self.processamento_mesa_df = pd.read_csv(processamento_mesa_url, delimiter='\t')
        self.processamento_sem_class_df = pd.read_csv(processamento_sem_class_url, delimiter='\t')

        union_select = '''
        select 'Viníferas' as classificacao, nullif(substr(control, 1, instr(control, '_') - 1), '') as categoria, * from processamento_viniferas_df

        union all

        select 'Americanas e híbridas' as classificacao, nullif(substr(control, 1, instr(control, '_') - 1), '') as categoria, * from processamento_americanas_df

        union all

        select 'Uvas de mesa' as classificacao, nullif(substr(control, 1, instr(control, '_') - 1), '') as categoria, * from processamento_mesa_df

        union all

        select 'Sem classificação' as classificacao, nullif(substr(control, 1, instr(control, '_') - 1), '') as categoria, * from processamento_sem_class_df
        '''

        self.processamento_class_cat_df = self._pysqldf(union_select).bfill()
        self.processamento_class_cat_df['processamento_id'] = self.processamento_class_cat_df.index + 1

        self._criar_processamento_categoria()
        self._criar_processamento_cultivar()
        self._criar_processamento_ano()

    def _criar_processamento_ano(self):
        # drop 2022 ->
        # Os dados disponibilizados pelo SISDEVIN no ano de 2022 estão agregados
        # [Uvas viníferas: 99.738.086; Uvas americanas ou híbridas: 565.243.922]

        self.processamento_anos_df = (
            self.processamento_class_cat_df
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
          categoria,
          cultivar
        from
          processamento_class_cat_df
        where
          control not like '%!_%' escape '!'
        '''

        self.processamento_categoria_df = self._pysqldf(processamento_categoria)

    def _criar_processamento_cultivar(self):
        processamento_cultivar = '''
        select
          processamento_id,
          classificacao,
          categoria,
          cultivar
        from
          processamento_class_cat_df
        where
          control like '%!_%' escape '!'
        '''

        self.processamento_cultivar_df = self._pysqldf(processamento_cultivar)
