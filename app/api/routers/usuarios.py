"""Endpoints de usuário: cadastro, login e quem sou eu."""
 
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import UsuarioAtual, obter_usuario_servico

from app.schemas.usuario import SessaoOut, UsuarioCreate, UsuarioLogin, UsuarioOut

from app.services.usuario import UsuarioServico
 
router = APIRouter(prefix="/usuarios", tags=["Usuários"])
 
 
@router.post(

    "",

    response_model=UsuarioOut,

    status_code=201,

    summary="Cadastrar usuário",

    responses={409: {"description": "E-mail já cadastrado"}},

)

def cadastrar_usuario(

    dados: UsuarioCreate,

    servico: Annotated[UsuarioServico, Depends(obter_usuario_servico)],

):

    """Cria uma conta. O cadastro não faz login automaticamente."""

    return servico.cadastrar(dados.nome, dados.email, dados.senha)
 
 
@router.post(

    "/login",

    response_model=SessaoOut,

    summary="Entrar no sistema",

    responses={401: {"description": "E-mail ou senha incorretos"}},

)

def entrar(

    dados: UsuarioLogin,

    servico: Annotated[UsuarioServico, Depends(obter_usuario_servico)],

):

    """Realiza o login. No /docs, o token retornado é usado no botão Authorize."""

    sessao = servico.entrar(dados.email, dados.senha)

    return SessaoOut(

        access_token=sessao.token.valor,

        expira_em=sessao.token.expira_em,

        usuario=UsuarioOut.model_validate(sessao.usuario),

    )
 
 
@router.get(

    "/me",

    response_model=UsuarioOut,

    summary="Consultar o usuário logado",

    responses={401: {"description": "Não autenticado ou token inválido"}},

)

def quem_sou_eu(usuario: UsuarioAtual) -> UsuarioOut:

    """Devolve os dados do perfil do usuário autenticado pelo token."""

    return usuario
 