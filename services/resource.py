'''
PATRÓN DE DISEÑO: DECORATOR (Decorador) - US-04 Recursos de Soporte

IProposalComponent: interfaz base del componente
BaseProposalComponent: la ILC sin recursos extra
ProposalResourceDecorator: decorador abstracto para envolver un IProposalComponent
CommentDecorator: agrega un recurso de tipo COMENTARIO
DocumentDecorator: agrega un recurso de tipo DOCUMENTO
ModificationDecorator: agrega un recurso de tipo MODIFICACION
ResourceService: punto de entrada de recurso si la ILC está activa (instancia
el decorador adecuado según el tipo) y rechaza la operacion si la ILC no esta activa.
'''
from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

import storage
from domains.models import Resource, ResourceType, ProposalState



class IProposalComponent(ABC):
    @property
    @abstractmethod
    def proposal_id(self) -> str: ...

    @abstractmethod
    def get_description(self) -> str: ...


class BaseProposalComponent(IProposalComponent):
    def __init__(self, proposal_id: str):
        self._proposal_id = proposal_id
        p = storage.proposals.get(proposal_id)
        self._title = p.title if p else "ILC desconocida"

    @property
    def proposal_id(self) -> str:
        return self._proposal_id

    def get_description(self) -> str:
        print(f"[BaseProposalComponent] ILC base: '{self._title}'")
        return self._title

# Decorador de interfaz
class ProposalResourceDecorator(IProposalComponent):
    def __init__(self, component: IProposalComponent):
        self._component = component

    @property
    def proposal_id(self) -> str:
        return self._component.proposal_id

    def get_description(self) -> str:
        return self._component.get_description()

    def _persist(self, author_id: str, content: str, rtype: ResourceType) -> Resource:
        resource = Resource(
            id            = str(uuid.uuid4())[:8].upper(),
            proposal_id   = self.proposal_id,
            author_id     = author_id,
            resource_type = rtype,
            content       = content,
            created_at    = datetime.now(),
        )
        storage.resources.setdefault(self.proposal_id, []).append(resource)
        return resource

    @abstractmethod
    def apply(self, author_id: str, content: str) -> Resource: ...


#Decorador para cada tipo de recurso
class CommentDecorator(ProposalResourceDecorator):
    def get_description(self) -> str:
        return self._component.get_description() + " + [Comentario]"

    def apply(self, author_id: str, content: str) -> Resource:
        print(f"[CommentDecorator] Adjuntando comentario a la ILC '{self.proposal_id}'...")
        r = self._persist(author_id, content, ResourceType.COMENTARIO)
        print(f"[CommentDecorator] Comentario registrado — ID: {r.id}")
        return r


class DocumentDecorator(ProposalResourceDecorator):
    def get_description(self) -> str:
        return self._component.get_description() + " + [Documento]"

    def apply(self, author_id: str, content: str) -> Resource:
        print(f"[DocumentDecorator] Adjuntando documento a la ILC '{self.proposal_id}'...")
        r = self._persist(author_id, content, ResourceType.DOCUMENTO)
        print(f"[DocumentDecorator] Documento registrado — ID: {r.id}")
        return r


class ModificationDecorator(ProposalResourceDecorator):
    def get_description(self) -> str:
        return self._component.get_description() + " + [Modificacion]"

    def apply(self, author_id: str, content: str) -> Resource:
        print(f"[ModificationDecorator] Adjuntando modificacion a la ILC '{self.proposal_id}'...")
        r = self._persist(author_id, content, ResourceType.MODIFICACION)
        print(f"[ModificationDecorator] Modificacion registrada — ID: {r.id}")
        return r


#Entrada del reurso seleccionado

class ResourceService:
    _DECORATORS = {
        "COMENTARIO":   CommentDecorator,
        "DOCUMENTO":    DocumentDecorator,
        "MODIFICACION": ModificationDecorator,
    }

    def add(self, proposal_id: str, author_id: str, tipo: str, content: str) -> Resource:
        print(f"\n[ResourceService] Iniciando adicion de recurso tipo '{tipo}'...")

        proposal = storage.proposals.get(proposal_id)
        if not proposal:
            raise ValueError("ILC no encontrada.")
        if proposal.state != ProposalState.ACTIVA:
            raise ValueError(
                f"No se pueden agregar recursos: la ILC esta en estado '{proposal.state.value}'."
            )
        if not content.strip():
            raise ValueError("El contenido no puede estar vacio.")

        base          = BaseProposalComponent(proposal_id)
        decorator_cls = self._DECORATORS.get(tipo, CommentDecorator)
        decorated     = decorator_cls(base)

        print(f"[ResourceService] Descripcion decorada: {decorated.get_description()}")
        resource = decorated.apply(author_id, content.strip())

        print(f"[ResourceService] Recurso '{tipo}' anadido exitosamente.\n")
        return resource
