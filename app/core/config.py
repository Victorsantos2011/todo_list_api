from dataclasses import dataclass
from functools import lru_cache
import os
from dotenv import load_dotenv
 
load_dotenv()
 
 
class ConfiguracaoInvalida(RuntimeError):
    """Exceção para quando a configuração é inválida ou inexistente."""
 
    pass
 
 
@dataclass(frozen=True)
class Configuracao:
    database_url: str = ""
    jwt_secret: str = ""
    jwt_expira_minutos: int = 120
 
    @classmethod
    def do_ambiente(cls) -> "Configuracao":
        return cls(
            database_url=os.getenv("DATABASE_URL", "").strip(),
            jwt_secret=os.getenv("JWT_SECRET", "").strip(),
            jwt_expira_minutos=int(os.getenv("JWT_EXPIRA_MINUTOS", "120")),
        )
 
    @property
    def url_banco(self) -> str:
        if not self.database_url:
            raise ConfiguracaoInvalida(
                "A DATABASE_URL não foi configurada. Copie o arquivo .env.example para .env e tente novamente."
            )
        return self.database_url
 
    def segredo_jwt(self) -> str:
        if len(self.jwt_secret) < 32:
            raise ConfiguracaoInvalida(
                "O JWT_SECRET não foi configurado ou é muito curto (mínimo 32 caracteres).\n"
                "Gere um segredo forte rodando:\n"
                '  python -c "import secrets; print(secrets.token_hex(32))"'
            )
        return self.jwt_secret
 
 
@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao.do_ambiente()
 