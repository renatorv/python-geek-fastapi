# Configurações gerais utilizadas em todo o projeto.
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
        Configurações gerais utilizadas na aplicação
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:159753@localhost:5432/faculdade"
    DBBaseModel = declarative_base()
    
    class Config:
        case_sensitive = True
        
# INSTANCIA O OBJETO, 
# QUE PODE SER UTILIZADO EM QQ LOCAL DA APLICAÇÃO
settings = Settings()