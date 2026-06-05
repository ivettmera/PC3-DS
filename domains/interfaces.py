'''
Contratos e interfaces del sistema
'''
from abc import ABC, abstractmethod


class ICryptoService(ABC):
    '''Contrato para sellar criptográficamente un expediente'''

    @abstractmethod
    def seal(self, proposal_id: str, data: dict) -> str:
        '''Devuelve el hash del expediente sellado.'''


class INotificationService(ABC):
    '''Contrato para enviar alertas a colectivos y ciudadanos.'''

    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        '''Envía un correo electrónico al destinatario indicado con asunto y cuerpo.'''


class ICongressClient(ABC):
    '''Contrato para transmitir expedientes sellados a la Oficina del Congreso.'''

    @abstractmethod
    def transmit(self, package: dict) -> bool:
        '''Envía el expediente sellado al Congreso y retorna True si la transmisión fue exitosa.'''


class ISignatureService(ABC):
    '''Contrato para el servicio de firma digital de ciudadanos.'''

    @abstractmethod
    def sign(self, citizen_id: str, proposal_id: str) -> bool:
        '''Registra la firma de un ciudadano para una propuesta dada. 
        Retorna True si la firma es válida y se registró correctamente.'''
