'''
Contiene las estructuras base de datos del sistema
'''
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional


class ProposalState(Enum):
    BORRADOR   = "Borrador"
    ACTIVA     = "Activa"
    SELLADA    = "Sellada"
    ARCHIVADA  = "Archivada"


class ResourceType(Enum):
    COMENTARIO   = "Comentario"
    DOCUMENTO    = "Documento"
    MODIFICACION = "Modificacion"


@dataclass
class Collective:
    id:             str
    name:           str
    ruc:            str
    representative: str
    email:          str
    approved:       bool = False


@dataclass
class Citizen:
    id:              str
    document_number: str
    name:            str
    email:           str


@dataclass
class Proposal:
    SIGNATURE_THRESHOLD: int = field(default=25_000, init=False, repr=False)
    DAYS_LIMIT:          int = field(default=90,     init=False, repr=False)

    id:              str
    title:           str
    motivation:      str
    articles:        str
    category:        str
    collective_id:   str
    state:           ProposalState    = ProposalState.BORRADOR
    signature_count: int              = 0
    created_at:      datetime         = field(default_factory=datetime.now)
    start_date:      Optional[date]   = None
    deadline:        Optional[date]   = None
    seal_hash:       Optional[str]    = None
    sealed_at:       Optional[datetime] = None


@dataclass
class Signature:
    id:              str
    citizen_id:      str
    proposal_id:     str
    timestamp:       datetime
    integrity_hash:  str


@dataclass
class Resource:
    id:            str
    proposal_id:   str
    author_id:     str
    resource_type: ResourceType
    content:       str
    created_at:    datetime
    filename:      Optional[str] = None
