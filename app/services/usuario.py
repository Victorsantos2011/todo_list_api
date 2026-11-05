"""Operações de cadastro, login e identificação de usuários."""
 
from dataclasses import dataclass

from app.core.exceptions import (

    CredenciaisInvalidas,

    EmailJaCadastrado,

    TokenInvalido,

)

from app.core.security import HashDeSenha, TokenEmitido, TokenJWT

from app.models.usuario import Usuario

from app.repositories.usuario import UsuarioRepositorio
 
 
@dataclass(frozen=True)

class Sessao:

    usuario: Usuario

    token: TokenEmitido
 
 
class UsuarioServico:

    def __init__(

        self,

        repositorio: UsuarioRepositorio,

        hasher: HashDeSenha,

        tokens: TokenJWT | None = None,

    ):

        self._repositorio = repositorio

        self._hasher = hasher

        self._tokens = tokens
 
    def cadastrar(self, nome: str, email: str, senha: str) -> Usuario:

        """

        Cadastra um novo usuário.
 
        Raises:

            EmailJaCadastrado: Se o e-mail já estiver em uso.

        """

        if self._repositorio.email_existe(email):

            raise EmailJaCadastrado()
 
        usuario = Usuario(nome=nome, email=email)

        usuario.definir_senha(senha, self._hasher)

        return self._repositorio.salvar(usuario)
 
    def autenticar(self, email: str, senha: str) -> Usuario:

        """

        Verifica e-mail e senha.
 
        Raises:

            CredenciaisInvalidas: Se as credenciais estiverem incorretas.

        """

        usuario = self._repositorio.buscar_por_email(email)

        if usuario is None or not usuario.senha_confere(senha, self._hasher):

            raise CredenciaisInvalidas()

        return usuario
 
    def entrar(self, email: str, senha: str) -> Sessao:

        """

        Realiza o login do usuário e emite o token de acesso.
 
        Raises:

            CredenciaisInvalidas: Se as credenciais estiverem incorretas.

        """

        usuario = self.autenticar(email, senha)

        token = self._exigir_tokens().emitir(usuario.id)

        return Sessao(usuario=usuario, token=token)
 
    def usuario_do_token(self, token: str) -> Usuario:

        """

        Identifica o usuário a partir do token de acesso.
 
        Raises:

            TokenInvalido: Se o token for inválido, vencido ou o usuário não existir.

        """

        usuario_id = self._exigir_tokens().ler(token)

        usuario = self._repositorio.buscar_por_id(usuario_id)

        if usuario is None:

            raise TokenInvalido()

        return usuario
 
    def _exigir_tokens(self) -> TokenJWT:

        if self._tokens is None:

            raise RuntimeError("Serviço de usuários montado sem emissor de tokens.")

        return self._tokens
 