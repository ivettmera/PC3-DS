'''
Diccionarios y listas globales que actúan como base de datos.
Almacena las ILCs creadas, firmas válidas y usuarios de prueba.
'''
from datetime import date, timedelta

import storage
from domains.models import Collective, Citizen, Proposal, ProposalState
from services.proposal import ProposalFacade


def seed_demo_data() -> None:
    '''Carga datos de prueba para la demo de la PC'''

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
    ciudadano3 = Citizen(
        id="CIT-003",
        document_number="46395542",
        name="Ernesto Coronado",
        email="ernesto.coronado@correo.pe",
    )
    storage.citizens[ciudadano1.id] = ciudadano1
    storage.citizens[ciudadano2.id] = ciudadano2
    storage.citizens[ciudadano3.id] = ciudadano3

    print("[DB] Datos de demostración cargados en memoria.")
    print(f"[DB]   Colectivos : {len(storage.collectives)}")
    print(f"[DB]   Ciudadanos : {len(storage.citizens)}")

    facade = ProposalFacade(notification_service=None)

    print("\n[DB] Generando iniciativas automáticas para la demo...")

    # ILC 1
    p1 =facade.create_draft(
        title="Ley de Protección",
        category="Medio Ambiente",
        motivation="El agua potable de nuestras ciudades depende de la intangibilidad de las zonas altas donde nacen los ríos, hoy amenazadas por la actividad industrial irresponsable.",
        articles="Artículo 1.— Declárese de prioridad nacional e intangibles las cabeceras de cuenca hidrográfica del territorio peruano.\nArtículo 2.— Prohíbase cualquier actividad extractiva a menos de 10 kilómetros de origen de un recurso hídrico.",
        collective_id="COL-003",
        start_date = date(2025, 10, 22),
        deadline= date(2025, 10, 22) + timedelta(days=90),
    )

    # ILC2
    p2 = facade.create_draft(
        title="Plan Nacional de Alfabetización Digital en Escuelas Rurales",
        category="Educación",
        motivation="Existe una brecha educativa enorme entre los estudiantes urbanos y rurales por falta de infraestructura tecnológica y capacitación docente en entornos digitales.",
        articles="Artículo 1.— Garantizar conectividad satelital gratuita al 100% de colegios públicos rurales.\nArtículo 2.— Incorporar el curso obligatorio de Competencias Digitales desde el nivel primario.",
        collective_id="COL-005",
        start_date = date(2024, 10, 22),
        deadline= date(2024, 10, 22) + timedelta(days=90)
    )

    if p1:
        storage.signatures[p1.id] = ["CIT-001", "CIT-002"]
        p1.signature_count = 3
        p1.state = ProposalState.SELLADA
        storage.proposals[p1.id] = p1 

    if p2:
        storage.proposals[p2.id] = p2