'''
PATRÓN DE DISEÑO: FACADE - US-02 Creación de ILC

ProposalFacade oculta la complejidad de crear y publicar una ILC, exponiendo una interfaz simple al cliente (ruta Flask)
  _ContentValidator : valida campos y longitud del articulado
  _StateManager     :  transiciona el estado Borrador → Activa
  _DeadlineScheduler : asigna start_date y deadline (desde hoy a + 90 días)
  INotificationService (inyectado) : avisa al colectivo por correo
'''
from __future__ import annotations
import uuid
from datetime import date, timedelta

import storage
from domains.models import Proposal, ProposalState
from domains.interfaces import INotificationService

class _ContentValidator:
    MAX_ARTICLES_LEN = 50_000

    def validate(self, title: str, motivation: str, articles: str) -> tuple[bool, str]:
        print("[ContentValidator] Verificando campos obligatorios...")
        if not title.strip():
            return False, "El título no puede estar vacío."
        if not motivation.strip():
            return False, "La motivación no puede estar vacía."
        if not articles.strip():
            return False, "El articulado no puede estar vacío."
        print(f"[ContentValidator] Longitud del articulado: {len(articles)} chars.")
        if len(articles) > self.MAX_ARTICLES_LEN:
            return False, f"El articulado supera el límite de {self.MAX_ARTICLES_LEN:,} caracteres."
        print("[ContentValidator] Validación exitosa.")
        return True, ""


class _StateManager:
    def activate(self, proposal: Proposal) -> None:
        print(f"[StateManager] Transición: {proposal.state.value} → Activa")
        proposal.state = ProposalState.ACTIVA


class _DeadlineScheduler:
    DAYS = 90

    def assign(self, proposal: Proposal) -> None:
        proposal.start_date = date.today()
        proposal.deadline   = date.today() + timedelta(days=self.DAYS)
        print(f"[DeadlineScheduler] Inicio: {proposal.start_date}  |  Límite: {proposal.deadline}")


class ProposalFacade:
    '''
    Interfaz simplificada para create y publicar una ILC.
    El cliente (ruta Flask) llama a create_and_publish() sin conocer los subsistemas.
    '''

    def __init__(self, notification_service: INotificationService):
        self._validator = _ContentValidator()
        self._state_mgr = _StateManager()
        self._scheduler = _DeadlineScheduler()
        self._notifier  = notification_service

    def create_and_publish(
        self,
        title:         str,
        motivation:    str,
        articles:      str,
        category:      str,
        collective_id: str,
    ) -> tuple[bool, str, Proposal | None]:
        '''
        Orquesta validación, estado, plazo y notificación.
        Retorna: (éxito, mensaje_error, propuesta).
        '''
        print("\n[ProposalFacade] ── Iniciando creación de ILC ──")

        ok, error = self._validator.validate(title, motivation, articles)
        if not ok:
            print(f"[ProposalFacade] Abortado: {error}")
            return False, error, None

        proposal = Proposal(
            id            = str(uuid.uuid4())[:8].upper(),
            title         = title.strip(),
            motivation    = motivation.strip(),
            articles      = articles.strip(),
            category      = category,
            collective_id = collective_id,
        )
        print(f"[ProposalFacade] Borrador creado — ID: {proposal.id}")

        self._scheduler.assign(proposal)
        self._state_mgr.activate(proposal)

        storage.proposals[proposal.id]  = proposal
        storage.signatures[proposal.id] = []
        storage.resources[proposal.id]  = []
        print(f"[ProposalFacade] ILC '{proposal.id}' guardada en almacenamiento.")

        colectivo = storage.collectives.get(collective_id)
        if colectivo:
            self._notifier.send_email(
                to      = colectivo.email,
                subject = f"ILC publicada: {proposal.title}",
                body    = (
                    f"Su iniciativa '{proposal.title}' ya está activa. "
                    f"Tiene hasta el {proposal.deadline} para recolectar 25 000 firmas."
                ),
            )

        print("[ProposalFacade] ── ILC publicada exitosamente ──\n")
        return True, "", proposal
    
    def create_draft(self, title: str, motivation: str, articles: str, category: str, collective_id: str, start_date: date, deadline: date) -> Proposal:
        '''
        Crea propuestas de prueba
        '''
        proposal = Proposal(
            id            = str(uuid.uuid4())[:8].upper(),
            title         = title.strip(),
            motivation    = motivation.strip(),
            articles      = articles.strip(),
            category      = category,
            collective_id = collective_id,
            start_date    = start_date,
            deadline      = deadline,
        )
        if deadline > date.today():
            proposal.state = ProposalState.ACTIVA
        else:
            proposal.state = ProposalState.ARCHIVADA
        

        print(f"[ProposalFacade] Borrador creado — ID: {proposal.id}")
        return proposal