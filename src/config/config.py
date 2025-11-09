import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Config:
    CHAVE_API: Final[str] = os.environ['CHAVE_API']
    URL_API_SPTRANS: Final[str] = os.environ['URL_API_SPTRANS']
