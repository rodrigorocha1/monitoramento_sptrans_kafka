import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Config:
    CHAVE_API: Final[str] = os.environ['CHAVE_API']
    URL_API_SPTRANS: Final[str] = os.environ['URL_API_SPTRANS']
    URL_KAFKA: Final[str] = os.environ['URL_KAFKA']
    URL_KSQL: Final[str] = os.environ['URL_KSQL']
