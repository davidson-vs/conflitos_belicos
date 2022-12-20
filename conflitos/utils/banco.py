import psycopg2 as pg
 
class Banco:
    @staticmethod
    def connection(host: str = 'localhost', database:str = 'db_conflitos_belicos', user:str ='postgres', password: str = "virtual10"):
        try:
            cxn = pg.connect(f'host = {host} dbname={database} user = {user} password = {password} ')
            if cxn :
                return cxn
        except Exception as cxn_error:
            print(f'erro ao se conectar ao banco de dados: {cxn_error}')

    @staticmethod
    def execute_query(cxn, query, params=None, many=False, persistence=False):
        cursor = cxn.cursor()
        try:
            if many is False:
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
            else:
                cursor.fast_executemany = True
                cursor.executemany(query, params)

            if persistence:
                cxn.commit()
                if cursor.rowcount > 1:
                    print('Affected rows: {}'.format(cursor.rowcount))
        except pg.IntegrityError as ie:
            print('An integrity error has occurred.')
            raise ie
        except Exception as e:
            print("Error while running a query execution: {}".format(e))
            raise Exception("Error while running a query execution: {}".format(e))
        finally:
            cursor.close()
            cxn.close()

    @staticmethod
    def get_multiple_result(cxn, query, *args):
        """
        Método que retorna multiplos resultados do banco
        :param cxn: pyodbc cxn obj
        :param query: str
        :param args: tuple
        :return: dataset
        """
        cursor = cxn.cursor()
        results = []  # Lista para armazenamento dos resultados junto os nomes de colunas
        try:
            cursor.execute(query, *args)
            columns = [column[0] for column in cursor.description]  # Capturando as colunas do dataset
            for row in cursor.fetchall():  # Para cada linha do resultado do banco, mesclar o resultado do banco junto ao nome da coluna.
                results.append(dict(zip(columns, row)))
            return results
        except Exception as error:
            raise Exception('Erro ao executar a query "{}" \n \n ERRO: {}'.format(query, error))
        finally:
            cursor.close()

    def execute_proceudure(self, cxn, query):
        no_count = 'SET NOCOUNT ON;'
        proc = no_count + query
        result = self.get_multiple_result(cxn, proc)
        return result
