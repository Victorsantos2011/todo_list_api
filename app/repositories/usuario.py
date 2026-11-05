from app.models.usuario import Usuario
from app.repositories.base import RepositorioBase
 
 
class UsuarioRepositorio(RepositorioBase[Usuario]):
    @property
    def modelo(self):
        return Usuario
 
    def buscar_por_email(self, email: str) -> Usuario | None:
        email_normalizado = Usuario.normalizar_email(email)
        return (
            self._sessao.query(Usuario)
            .filter(Usuario.email == email_normalizado)
            .first()
        )
 
    def email_existe(self, email: str) -> bool:
        """RN-01: Um e-mail não pode ser usado por dois usuários."""
        return self.buscar_por_email(email) is not None
 