"""Contrato JSON de usuário e de sessão (login)."""
 
from pydantic import Field, EmailStr, field_validator
from app.schemas.base import EsquemaDeEntrada, EsquemaDeSaida, DataHoraUTC
from app.core.security import LIMITE_BYTES_SENHA
 
 
class UsuarioCreate(EsquemaDeEntrada):
    nome: str = Field(min_length=1, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6)
 
    @field_validator("senha")
    @classmethod
    def validar_limite_bytes(cls, v: str) -> str:
        if len(v.encode("utf-8")) > LIMITE_BYTES_SENHA:
            raise ValueError(f"A senha não pode ultrapassar {LIMITE_BYTES_SENHA} bytes.")
        return v
 
 
class UsuarioOut(EsquemaDeSaida):
    id: int
    nome: str
    email: str
    criado_em: DataHoraUTC
 
 
class UsuarioLogin(EsquemaDeEntrada):
    email: EmailStr
    senha: str
 
 
class SessaoOut(EsquemaDeSaida):
    access_token: str
    token_type: str = "bearer"
    expira_em: DataHoraUTC
    usuario: UsuarioOut
 