"""
Exceções de domínio do sistema.
 
O domínio nunca lança HTTPException; ele lança as exceções deste arquivo,
e o main.py as traduz em códigos de status HTTP correspondentes.
"""
 
 
class ErroDeDominio(Exception):
    """Classe base para todas as exceções do domínio."""
 
    mensagem: str = "Ocorreu um erro no domínio."
 
    def __init__(self, mensagem: str | None = None):
        super().__init__(mensagem or self.mensagem)
        self.mensagem = mensagem or self.mensagem
 
 
# --- Família 404 (Recurso Não Encontrado) ---
 
 
class RecursoNaoEncontrado(ErroDeDominio):
    mensagem: str = "Recurso não encontrado."
 
 
class UsuarioNaoEncontrado(RecursoNaoEncontrado):
    mensagem: str = "Usuário não encontrado."
 
 
# --- Família 422 (Regra de Negócio / Entrada Inválida) ---
 
 
class RegraDeNegocioViolada(ErroDeDominio):
    mensagem: str = "Regra de negócio violada."
 
 
class ValorInvalido(RegraDeNegocioViolada):
    mensagem: str = "Valor fornecido é inválido."
 
 
# --- Família 409 e 401 (Conflito e Autenticação) ---
 
 
class EmailJaCadastrado(ErroDeDominio):
    mensagem: str = "Já existe uma conta com este e-mail."
 
 
class NaoAutenticado(ErroDeDominio):
    mensagem: str = "É preciso entrar na conta para continuar."
 
 
class CredenciaisInvalidas(NaoAutenticado):
    mensagem: str = "E-mail ou senha incorretos."
 
 
class TokenInvalido(NaoAutenticado):
    mensagem: str = "Sessão inválida. Entre novamente."
