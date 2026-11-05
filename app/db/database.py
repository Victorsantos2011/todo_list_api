from typing import Generator

from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker, Session

from sqlalchemy.pool import StaticPool

from app.core.config import obter_configuracao
 
def _opcoes_do_engine(url: str) -> dict:

    if url.startswith("sqlite"):

        return {

            "connect_args": {"check_same_thread": False},

            "poolclass": StaticPool,

        }

    return {"pool_pre_ping": True}
 
_url = obter_configuracao().url_banco

engine = create_engine(_url, echo=False, **_opcoes_do_engine(_url))
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
 
def criar_tabelas():

    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
 
def obter_sessao() -> Generator[Session, None, None]:

    sessao = SessionLocal()

    try:

        yield sessao

    finally:

        sessao.close()
 