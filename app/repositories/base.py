from abc import ABC, abstractmethod

from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session
 
Entidade = TypeVar("Entidade")
 
class RepositorioBase(ABC, Generic[Entidade]):

    def __init__(self, sessao: Session):

        self._sessao = sessao
 
    @property

    @abstractmethod

    def modelo(self) -> Type[Entidade]:

        pass
 
    def buscar_por_id(self, id: int) -> Entidade | None:

        return self._sessao.get(self.modelo, id)
 
    def salvar(self, entidade: Entidade) -> Entidade:

        self._sessao.add(entidade)

        self._sessao.commit()

        self._sessao.refresh(entidade)

        return entidade
 
    def remover(self, entidade: Entidade) -> None:

        self._sessao.delete(entidade)

        self._sessao.commit()
 