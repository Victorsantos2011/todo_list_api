"""Acesso aos dados de tarefa."""
 
from __future__ import annotations

from app.models import Tarefa

from app.repositories.base import RepositorioBase
 
 
class TarefaRepositorio(RepositorioBase[Tarefa]):

    """Acesso aos dados de tarefa."""
 
    @property

    def modelo(self) -> type[Tarefa]:

        return Tarefa
 
    def listar(self, usuario_id: int) -> list[Tarefa]:

        """Busca as tarefas do usuário, da mais recente para a mais antiga.

        O filtro pelo dono vai na consulta SQL (WHERE) para garantir que

        o banco só devolva as tarefas do usuário autenticado.

        """

        return (

            self._sessao.query(Tarefa)

            .filter(Tarefa.usuario_id == usuario_id)

            .order_by(

                Tarefa.criado_em.desc(),

                Tarefa.id.desc(),  # Desempate garanta ordem determinística

            )

            .all()

        )
 