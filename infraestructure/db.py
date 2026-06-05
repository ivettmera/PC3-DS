'''
Diccionarios y listas globales que actúan como base de datos efímera.
Almacena las ILCs creadas, firmas válidas y usuarios de prueba.
'''
import storage
from domains.models import Collective, Citizen, Proposal, ProposalState


def seed_demo_data() -> None:
    '''Carga datos de prueba para la DEMO de la PC'''

    colectivo = Collective(
        id="COL-001",
        name="Ciudadanos por el Cambio",
        ruc="20512345678",
        representative="Ana Torres",
        email="ana.torres@colectivo.pe",
        approved=True,
    )
    storage.collectives[colectivo.id] = colectivo

    ciudadano1 = Citizen(
        id="CIT-001",
        document_number="12345678",
        name="Luis Pérez",
        email="luis.perez@correo.pe",
    )
    ciudadano2 = Citizen(
        id="CIT-002",
        document_number="87654321",
        name="María Quispe",
        email="maria.quispe@correo.pe",
    )
    storage.citizens[ciudadano1.id] = ciudadano1
    storage.citizens[ciudadano2.id] = ciudadano2

    print("[DB] Datos de demostración cargados en memoria.")
    print(f"[DB]   Colectivos : {len(storage.collectives)}")
    print(f"[DB]   Ciudadanos : {len(storage.citizens)}")