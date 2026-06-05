'''
SERVICIO DE NOTIFICACIONES (Email/SMS)
Responsabilidad: Simular alertas automáticas a colectivos y ciudadanos.
Mensaje de consola: [NotificationService] Enviando correo electrónico a {email}
'''
from domains.interfaces import INotificationService


class NotificationService(INotificationService):
    '''
    Stub del servicio de notificaciones.
    En producción integraría con un proveedor SMTP/SMS real (p.ej. SendGrid, Twilio).
    '''

    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"[NotificationService] Enviando correo electrónico a: {to}")
        print(f"[NotificationService]   Asunto : {subject}")
        print(f"[NotificationService]   Cuerpo : {body[:80]}{'...' if len(body) > 80 else ''}")
        print(f"[NotificationService] Correo entregado correctamente.")

    def send_sms(self, phone: str, message: str) -> None:
        print(f"[NotificationService] Enviando SMS al número: {phone}")
        print(f"[NotificationService]   Mensaje: {message[:60]}{'...' if len(message) > 60 else ''}")
        print(f"[NotificationService] SMS enviado correctamente.")
