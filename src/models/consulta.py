from typing import List, Dict

from sqlalchemy import text
from sqlalchemy.engine import Row

from src.models.database import Database
from src.models.entities import Base


class Consulta:

    def __init__(self):
        self.__db = Database()
        Base.metadata.create_all(bind=self.__db.engine)

    def consulta(self, sql: str, params: Dict = None) -> List[Row]:
        """
        Executa um SELECT customizado e retorna uma lista de linhas (Row).
        """

        session = self.__db.obter_sessao()
        stmt = text(sql)

        try:
            result = session.execute(stmt, params or {}).fetchall()


            return list(result)
        except Exception as e :
            print(e)
            return []
        finally:
            session.close()
