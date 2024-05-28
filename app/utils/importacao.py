import pandas as pd
from pandasql import sqldf
from unidecode import unidecode


class Importacao:

    def _pysqldf(self, query):
        return sqldf(query, vars(self))

    def __init__(self):
        self._iniciar_importacao()

    def _iniciar_importacao(self):
        imp_vinho_url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"
        imp_espumante_url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv"
        imp_fresca_url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv"
        imp_passa_url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv"
        imp_suco_url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv"

        self.imp_vinho_df = pd.read_csv(imp_vinho_url, delimiter=';')
        self.imp_espumante_df = pd.read_csv(imp_espumante_url, delimiter=';')
        self.imp_fresca_df = pd.read_csv(imp_fresca_url, delimiter=';')
        self.imp_passa_df = pd.read_csv(imp_passa_url, delimiter=';')
        self.imp_suco_df = pd.read_csv(imp_suco_url, delimiter=';')

        union_select = '''
        select 'Vinho de Mesa' as classificacao, * from imp_vinho_df

        union all

        select 'Espumantes' as classificacao, * from imp_espumante_df

        union all

        select 'Uvas frescas' as classificacao, * from imp_fresca_df

        union all

        select 'Uvas passas' as classificacao, * from imp_passa_df

        union all

        select 'Suco de uva' as classificacao, * from imp_suco_df
        '''

        self.imp_class_df = self._pysqldf(union_select)
        self.imp_class_df['importacao_id'] = self.imp_class_df.index + 1
        self.imp_class_df['pais'] = self.imp_class_df['País'].apply(lambda x: unidecode(x))

        self._criar_quantidade_importacao()
        self._criar_valores_importacao()

    def _criar_quantidade_importacao(self):
        self.quantidade_importacao_df = (
            self.imp_class_df
            .drop(
                [col for col in self.imp_class_df.columns if '.1' in col or col in ['Id', 'País', 'importacao_id']],
                axis=1
            )
            .melt(
                id_vars=['classificacao', 'pais'],
                var_name='ano',
                value_name='quantidade'
            )
        )

    def _criar_valores_importacao(self):
        self.valores_importacao_df = (
            self.imp_class_df
            .drop(
                [col for col in self.imp_class_df.columns if col.isnumeric() or col in ['Id', 'País', 'importacao_id']],
                axis=1
            )
            .melt(
                id_vars=['classificacao', 'pais'],
                var_name='ano',
                value_name='valor'
            )
        )

        self.valores_importacao_df['ano'] = self.valores_importacao_df['ano'].apply(lambda ano: ano.replace('.1', ''))
