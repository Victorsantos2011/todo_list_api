from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
 
from app.core.config import obter_configuracao
from app.core.exceptions import NaoAutenticado
from app.core.security import HashBcrypt, HashDeSenha, TokenJWT
from app.db.database import obter_sessao
from app.models.usuario import Usuario
from app.repositories.usuario import UsuarioRepositorio
from app.services.usuario import UsuarioServico
 
# auto_error=False garante que a falta de token vire NaoAutenticado
# e passe pelo mesmo tratador de erros de domínio do main.py.
_esquema_bearer = HTTPBearer(
    auto_error=False, description="Token recebido no login"
)
 
 
def obter_hasher() -> HashDeSenha:
    return HashBcrypt()
 
 
def obter_tokens() -> TokenJWT:
    config = obter_configuracao()
    return TokenJWT(config.segredo_jwt(), config.jwt_expira_minutos)
 
 
def obter_usuario_servico(
    sessao: Annotated[Session, Depends(obter_sessao)],
    hasher: Annotated[HashDeSenha, Depends(obter_hasher)],
    tokens: Annotated[TokenJWT, Depends(obter_tokens)],
) -> UsuarioServico:
    return UsuarioServico(UsuarioRepositorio(sessao), hasher, tokens)
 
 
def obter_usuario_atual(
    credenciais: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)
    ],
    servico: Annotated[UsuarioServico, Depends(obter_usuario_servico)],
) -> Usuario:
    if credenciais is None:
        raise NaoAutenticado()
    return servico.usuario_do_token(credenciais.credentials)
 
 
# Atalho para uso direto nos endpoints das rotas
UsuarioAtual = Annotated[Usuario, Depends(obter_usuario_atual)]
