"""Exceções de domínio."""
class ErroDeDominio(Exception):
    """Classe base de todo erro previsto de negócio."""
     mensagem = "Não foi possivel concluir a operação."
     def __init__(self, mensagem: str | None = None):
        self.mensagem = mensagem or type(self).mensagem
        super().__init__(self.mensagem)
        
 
# --- Família 404 (Recurso Não Encontrado) ---
 class RecursoNaoEncontrado(ErroDeDominio):
    """Pediram um registro que não existe."""
    mensagem = "Recurso não encontrado."
 class UsuarioNaoEncontrado(RecursoNaoEncontrado):
    mensagem = "Usuário não encontrado."
class UsuarioNaoEncontrado(RecursoNaoEncontrado):
    mensagem: str = "Usuário não encontrado."
 
 class RegraDeNegocioViolada(ErroDeDominio):
    """A operação é compreensivel, mas contraria uma regra do negócio."""
    mensagem = "Operação recusada por uma regra de negócio."
class TituloObrigatorio(RegraDeNegocioViolada):
    mensagem = "o titulo da tarefa não pode ficar vazio."
    class TituloOrigatorio(RegraDeNegocioViolada):
        """Valor fora do conjunto aceito por um capo do dominio."""
        mensagem = "Valor inválido para o campo."
 

 
 class EmilJaCadastrado(ErroDeDominio):
     """RN-01: um e-mail não pode ser usado por dois usrios.
     A mensagem é a mesma que o front-end já exibe hoje no cadastro.
     """
     mensagem = "Já existe uma conta com este e-mail."
     class NaoAutenticado(ErroDeDominio):
        ""'Familia dos erros de identidade - a camada HTTP traduz em 401."""
        mensagem = "È preciso entrar na conta para continuar."
        class CredenciaisInvalidas(NaoAutenticado):
            """E-mail inexistente ou senha incorreta.
            A mensagem é deliberadamente a mesa nos dois casos: dizer que o e-mail
            não existe revelaria a um atacante quais endereços estão cadastrados.
            """
            mensagem = "E-mail ou senha incorretos."
            class TokenInvalido(NaoAutenticado):
                """Token de acesso ausente, expirado, adulterado ou de usuário removido.""'
                mensagem = "Sessão inválida. Entre novamente."
 
 
