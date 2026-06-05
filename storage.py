'''
Diccionarios y listas globales que actúan como base de datos efímera.
Almacena de forma centralizada las ILCs creadas, firmas válidas y usuarios de prueba.
'''
from domains.models import Proposal, Signature, Collective, Citizen, Resource

proposals:   dict[str, Proposal]   = {}
signatures:  dict[str, list[Signature]] = {}
collectives: dict[str, Collective]  = {}
citizens:    dict[str, Citizen]     = {}
resources:   dict[str, list[Resource]]  = {} 
