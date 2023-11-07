from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

### SEM O .ENV, LEMBRAR DE CRIAR O .ENV_EXAMPLE
senha = 'senha'
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:{senha}@localhost/teste"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
