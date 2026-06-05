'''
PATRÓN DE DISEÑO: PROXY de protección - US-03 Firma Digital
RealSignatureService : persiste la firma en storage sin validación
SignatureProxy : actua como un guardian queintercepta sign() y aplica dos controles:
    -la ILC debe estar en estado Activa
    -el ciudadano no puede haber firmado antes (unicidad)
  Si las validaciones pasan, delega a RealSignatureService.
  Si la firma alcanza el umbral, ejecuta sellado cripto y envío al Congreso.
'''
from __future__ import annotations
import uuid
from datetime import datetime, timezone

import storage
from domains.models import Signature, ProposalState
from domains.interfaces import ISignatureService, ICryptoService, INotificationService, ICongressClient

#Para la demo, el umbral es bajo para mostrar el sellado en acción
DEMO_THRESHOLD = 3

class RealSignatureService(ISignatureService):
    def sign(self, citizen_id: str, proposal_id: str) -> bool:
        sig = Signature(
            id             = str(uuid.uuid4())[:8].upper(),
            citizen_id     = citizen_id,
            proposal_id    = proposal_id,
            timestamp      = datetime.now(timezone.utc),
            integrity_hash = f"h-{citizen_id[:4]}-{proposal_id[:4]}-{uuid.uuid4().hex[:6]}",
        )
        storage.signatures[proposal_id].append(sig)
        storage.proposals[proposal_id].signature_count += 1

        count = storage.proposals[proposal_id].signature_count
        print(f"[RealSignatureService] Firma registrada — ID: {sig.id}")
        print(f"[RealSignatureService] Ciudadano: {citizen_id}  |  ILC: {proposal_id}")
        print(f"[RealSignatureService] Contador actualizado: {count} firmas")
        return True


class SignatureProxy(ISignatureService):

    def __init__(
        self,
        crypto_service:       ICryptoService,
        notification_service: INotificationService,
        congress_client:      ICongressClient,
    ):
        self._real     = RealSignatureService()
        self._crypto   = crypto_service
        self._notifier = notification_service
        self._congress = congress_client

    def sign(self, citizen_id: str, proposal_id: str) -> bool:
        print(f"\n[SignatureProxy] Interceptando solicitud de firma...")

        #ILC existe y está activa
        proposal = storage.proposals.get(proposal_id)
        if not proposal:
            print("[SignatureProxy] RECHAZADO — ILC no encontrada.")
            raise ValueError("Iniciativa no encontrada.")
        if proposal.state != ProposalState.ACTIVA:
            print(f"[SignatureProxy] RECHAZADO — Estado: {proposal.state.value}")
            raise ValueError(f"La iniciativa no está activa (estado: {proposal.state.value}).")

        #el ciudadano no ha firmado antes
        already_signed = any(
            s.citizen_id == citizen_id
            for s in storage.signatures.get(proposal_id, [])
        )
        if already_signed:
            print(f"[SignatureProxy] RECHAZADO — '{citizen_id}' ya firmó esta ILC.")
            raise ValueError("Ya firmaste esta iniciativa. Solo se permite una firma por ciudadano.")

        #validaciones superadas
        print("[SignatureProxy] Validaciones superadas. Delegando al servicio real...")
        self._real.sign(citizen_id, proposal_id)

        #criterio de sellado por umbral
        if proposal.signature_count >= DEMO_THRESHOLD:
            self._seal_and_submit(proposal)

        return True

    def _seal_and_submit(self, proposal) -> None:
        print(f"\n[SignatureProxy] UMBRAL ALCANZADO ({DEMO_THRESHOLD} firmas). Iniciando sellado...")

        #congelar la ILC
        proposal.state = ProposalState.SELLADA
        print("[SignatureProxy] ILC bloqueada — estado: Sellada.")

        #sellar con crypto el expediente
        package_data = {
            "proposal_id":     proposal.id,
            "title":           proposal.title,
            "collective_id":   proposal.collective_id,
            "signature_count": proposal.signature_count,
            "sealed_at":       datetime.now(timezone.utc).isoformat(),
        }
        seal_hash = self._crypto.seal(proposal.id, package_data)
        proposal.seal_hash = seal_hash
        proposal.sealed_at = datetime.now(timezone.utc)

        #enviar al congreso
        package_data["seal_hash"] = seal_hash
        self._congress.transmit(package_data)

        #notificar
        colectivo = storage.collectives.get(proposal.collective_id)
        if colectivo:
            self._notifier.send_email(
                to      = colectivo.email,
                subject = f"ILC '{proposal.title}' enviada al Congreso",
                body    = (
                    f"Su iniciativa alcanzó {proposal.signature_count} firmas y fue sellada.\n"
                    f"Hash: {seal_hash}"
                ),
            )

        print("[SignatureProxy] ── Sellado y envío completado ──\n")
