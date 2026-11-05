"""

Ponto de entrada da aplicação.
 
Cria o app, registra as rotas e traduz erros de domínio em respostas HTTP.

"""
 
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
 
from app.api.routers import usuarios

from app.core.config import obter_configuracao

from app.core.exceptions import (

    EmailJaCadastrado,

    ErroDeDominio,

    NaoAutenticado,

    RecursoNaoEncontrado,

    RegraDeNegocioViolada,

)

from app.db.database import criar_tabelas
 
STATUS_POR_ERRO: tuple[tuple[type[ErroDeDominio], int], ...] = (

    (RecursoNaoEncontrado, 404),

    (EmailJaCadastrado, 409),

    (NaoAutenticado, 401),

    (RegraDeNegocioViolada, 422),

    (ErroDeDominio, 400),

)
 
 
@asynccontextmanager

async def ciclo_de_vida(app: FastAPI):

    # Confere se o segredo do JWT está configurado antes de iniciar a API

    obter_configuracao().segredo_jwt()

    criar_tabelas()

    yield
 
 
app = FastAPI(

    title="TODO List API",

    version="0.5.0",

    lifespan=ciclo_de_vida,

)
 
app.include_router(usuarios.router)
 
 
@app.exception_handler(ErroDeDominio)

async def tratar_erro_de_dominio(_request: Request, excecao: ErroDeDominio):

    codigo = next(

        (codigo for tipo, codigo in STATUS_POR_ERRO if isinstance(excecao, tipo)),

        400,

    )

    # Exige padrão HTTP WWW-Authenticate apenas em respostas 401

    cabecalhos = {"WWW-Authenticate": "Bearer"} if codigo == 401 else None
 
    return JSONResponse(

        status_code=codigo,

        content={"detail": excecao.mensagem},

        headers=cabecalhos,

    )
 
 
@app.get("/")

def raiz():

    return {"mensagem": "API rodando com sucesso!"}
 