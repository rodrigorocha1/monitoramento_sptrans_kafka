import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class Database:
    def __init__(self):
        self.__caminho_base = os.path.join(os.getcwd(), 'docs', 'sptrans.db')
        self.engine = create_engine(url=f'sqlite:///{self.__caminho_base}')
        self.SessionLocal = sessionmaker(bind=self.engine)

    def obter_sessao(self) -> Session:
        return self.SessionLocal()
