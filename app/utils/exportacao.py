import pandas as pd
from pandasql import sqldf
from unidecode import unidecode


class Exportacao:

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_exportacao()

    def _iniciar_exportacao(self):
        exp_vinho_url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
        exp_espumante_url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv"
        exp_fresca_url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv"
        exp_suco_url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"

        self.exp_vinho_df = pd.read_csv(exp_vinho_url, delimiter=';')
        self.exp_espumante_df = pd.read_csv(exp_espumante_url, delimiter=';')
        self.exp_fresca_df = pd.read_csv(exp_fresca_url, delimiter=';')
        self.exp_suco_df = pd.read_csv(exp_suco_url, delimiter=';')

        union_select = '''
        select 'Vinhos de Mesa' as classificacao, * from exp_vinho_df

        union all

        select 'Espumantes' as classificacao, * from exp_espumante_df

        union all

        select 'Uvas frescas' as classificacao, * from exp_fresca_df

        union all

        select 'Suco de uva' as classificacao, * from exp_suco_df
        '''

        self.exp_class_df = self._pysqldf(union_select)
        self.exp_class_df['exportacao_id'] = self.exp_class_df.index + 1
        self.exp_class_df['pais'] = self.exp_class_df['País'].apply(lambda x: unidecode(x))

        self._criar_quantidade_exportacao()
        self._criar_valores_exportacao()

    def _criar_quantidade_exportacao(self):
        self.quantidade_exportacao_df = (
            self.exp_class_df
            .drop(
                [col for col in self.exp_class_df.columns if '.1' in col or col in ['Id', 'País', 'exportacao_id']],
                axis=1
            )
            .melt(
                id_vars=['classificacao', 'pais'],
                var_name='ano',
                value_name='quantidade'
            )
        )

    def _criar_valores_exportacao(self):
        self.valores_exportacao_df = (
            self.exp_class_df
            .drop(
                [col for col in self.exp_class_df.columns if col.isnumeric() or col in ['Id', 'País', 'exportacao_id']],
                axis=1
            )
            .melt(
                id_vars=['classificacao', 'pais'],
                var_name='ano',
                value_name='valor'
            )
        )

        self.valores_exportacao_df['ano'] = self.valores_exportacao_df['ano'].apply(lambda ano: ano.replace('.1', ''))
