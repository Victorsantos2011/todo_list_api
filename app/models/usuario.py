from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy.orm import validates

from app.db.database import Base

from app.core.datas import agora_utc

from app.core.security import HashDeSenha

from app.core.exceptions import ValorInvalido
 
class Usuario(Base):

    __tablename__ = "usuarios"
 
    id = Column(Integer, primary_key=True, autoincrement=True)

    nome = Column(String(120), nullable=False)

    email = Column(String(180), nullable=False, unique=True, index=True)

    _senha_hash = Column("senha_hash", String(255), nullable=False)

    criado_em = Column(DateTime(timezone=True), nullable=False, default=agora_utc)
 
    def __init__(self, *, nome: str, email: str):

        self.nome = nome

        self.email = self.normalizar_email(email)
 
    @staticmethod

    def normalizar_email(email: str) -> str:

        return email.strip().lower()
 
    def definir_senha(self, senha: str, hasher: HashDeSenha):

        self._senha_hash = hasher.gerar(senha)
 
    def senha_confere(self, senha: str, hasher: HashDeSenha) -> bool:

        return hasher.verificar(senha, self._senha_hash)
 
    @validates("nome")

    def _validar_nome(self, key, nome):

        if not nome or not nome.strip():

            raise ValorInvalido("O nome não pode ser vazio.")

        return nome.strip()
 
    def __repr__(self) -> str:

        return f"<Usuario(id={self.id}, email='{self.email}')>"
 