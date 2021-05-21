from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///devolutiva_pdm.db"
# PARA TROCAR PARA POSTGRES É SÓ MUDAR A LINHA CONFORME ABAIXO, COM A CONNECTION STRING
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    #o argumento abaixo é para permitir multithreading com o sqlite, pode remover no postgresql
    connect_args={"check_same_thread": False}
)

#sessão da database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base para os modelos
Base = declarative_base()