'''
CLIENTE DE OFICINA DEL CONGRESO
Responsabilidad: Simular el canal seguro de envío legislativo. Recibe el expediente
sellado y simula la respuesta de éxito con un acuse de recibo formal.
mensaje de consola: [CongressClient] Transmitiendo expediente sellado a comisiones...
'''
from datetime import datetime, timezone
from domains.interfaces import ICongressClient


class CongressClient(ICongressClient):
    '''
    Cliente que representa la Oficina del Congreso.
    '''

    def transmit(self, package: dict) -> bool:
        proposal_id = package.get("proposal_id", "N/A")
        seal_hash   = package.get("seal_hash",   "N/A")
        timestamp   = datetime.now(timezone.utc).isoformat()

        print(f"[CongressClient] Abriendo canal seguro hacia la Oficina del Congreso...")
        print(f"[CongressClient] Transmitiendo expediente sellado a comisiones...")
        print(f"[CongressClient]   ILC            : {proposal_id}")
        print(f"[CongressClient]   Hash de sellado: {seal_hash}")
        print(f"[CongressClient]   Firmantes      : {package.get('signature_count', 0)} firmas válidas")
        print(f"[CongressClient] Recibiendo acuse de recibo del Congreso...")
        print(f"[CongressClient] ACUSE OK — Expediente registrado en el Congreso a las {timestamp}.")

        return True
