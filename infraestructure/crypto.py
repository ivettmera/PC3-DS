'''
SERVICIO CRIPTOGRÁFICO
Simular el sellado digital
'''
from datetime import datetime, timezone
from domains.interfaces import ICryptoService


class CryptoService(ICryptoService):
    '''
    Servicio de sellado criptográfico de expedientes ILC.
    Para esta PC se simula el proceso de sellado con un hash ficticio que incluye
    el ID de la propuesta y un timestamp.
    '''

    def seal(self, proposal_id: str, data: dict) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()
        fake_hash = f"sha256-STUB-{proposal_id[:8]}-{timestamp}"

        print(f"[CryptoService] Iniciando proceso de sellado para ILC '{proposal_id}'...")
        print(f"[CryptoService] Serializando expediente ({len(data)} campos)...")
        print(f"[CryptoService] Calculando hash SHA-256 del expediente...")
        print(f"[CryptoService] Timestamp UTC registrado: {timestamp}")
        print(f"[CryptoService] Hash generado: {fake_hash}")
        print(f"[CryptoService] Expediente SELLADO. Ningún campo puede modificarse.")

        return fake_hash
