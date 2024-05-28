import pandas as pd
from pandasql import sqldf
from unidecode import unidecode


class Importacao:
    _quantidade_importacao_df: pd.DataFrame
    _valores_importacao_df: pd.DataFrame

    @property
    def quantidade(self):
        return self._quantidade_importacao_df.to_json(orient='records')

    @property
    def valor(self):
        return self._valores_importacao_df.to_json(orient='records')

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

        self._imp_vinho_df = pd.read_csv(imp_vinho_url, delimiter=';')
        self._imp_espumante_df = pd.read_csv(imp_espumante_url, delimiter=';')
        self._imp_fresca_df = pd.read_csv(imp_fresca_url, delimiter=';')
        self._imp_passa_df = pd.read_csv(imp_passa_url, delimiter=';')
        self._imp_suco_df = pd.read_csv(imp_suco_url, delimiter=';')

        union_select = '''
        select 'Vinho de Mesa' as classificacao, * from _imp_vinho_df

        union all

        select 'Espumantes' as classificacao, * from _imp_espumante_df

        union all

        select 'Uvas frescas' as classificacao, * from _imp_fresca_df

        union all

        select 'Uvas passas' as classificacao, * from _imp_passa_df

        union all

        select 'Suco de uva' as classificacao, * from _imp_suco_df
        '''

        self._imp_class_df = self._pysqldf(union_select)
        self._imp_class_df['importacao_id'] = self._imp_class_df.index + 1
        self._imp_class_df['pais'] = self._imp_class_df['País'].apply(lambda x: unidecode(x))

        self._criar_quantidade_importacao()
        self._criar_valores_importacao()

    def _criar_quantidade_importacao(self):
        self._quantidade_importacao_df = (
            self._imp_class_df
            .drop(
                [col for col in self._imp_class_df.columns if '.1' in col or col in ['Id', 'País', 'importacao_id']],
                axis=1
            )
            .melt(
                id_vars=['classificacao', 'pais'],
                var_name='ano',
                value_name='quantidade'
            )
        )

    def _criar_valores_importacao(self):
        self._valores_importacao_df = (
            self._imp_class_df
            .drop(
                [col for col in self._imp_class_df.columns if col.isnumeric() or col in ['Id', 'País', 'importacao_id']],
                axis=1
            )
            .melt(
                id_vars=['classificacao', 'pais'],
                var_name='ano',
                value_name='valor'
            )
        )

        self._valores_importacao_df['ano'] = self._valores_importacao_df['ano'].apply(lambda ano: ano.replace('.1', ''))
