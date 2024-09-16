from django.core.mail import send_mail  # Importe la fonctionnalité d'envoi de courrier électronique Django
from RoomQueSTIC import settings  # Importe les paramètres de configuration de l'application

def reservation_url(booked_room) -> str:
    return f'https://crestic.univ-reims.fr/reservations/roombooking/{booked_room.id}/edit/'

def greeting_template(booked_room) -> str:
    return f'Bonjour {booked_room.user.first_name},'

def booked_room_text_template(booked_room) -> str:
    text = f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n'
    return text

class MessageTemplate:

    def __init__(self, booking):
        self._booking = booking
        self._booking_type_name = 'Salle/Équipement'

    @property
    def greeting(self) -> str:
        return f'Bonjour {self._booking.user.first_name},'

    @property
    def default_text(self) -> str:
        text = f'Date: {self._booking.date}\n' \
              f'{self._booking_type_name}: {self.booked_item}\n' \
              f'Heure de début: {self._booking.startTime}\n' \
              f'Heure de fin: {self._booking.endTime}\n' \
              f'Groupe/Laboratoire: {self._booking.groups}\n' \
              f'Motif: {self._booking.motif}\n' \
              f'\n\nhttps://crestic.univ-reims.fr/reservations'
        return text

    @property
    def confirmation_text(self) -> str:
        return f'{self.default_text}\n\nhttps://crestic.univ-reims.fr/reservations'

    @property
    def confirmation_subject(self) -> str:
        return 'Votre réservation a bien été validée'

    @property
    def booked_item(self):
        return 'Catégorie inconnue'
    @property
    def notification_text(self) -> str:
        message = f'Une nouvelle réservation a été faite par {self._booking.user.first_name}' \
          f' {self._booking.user.last_name} ({self._booking.user.email}).\n' \
          f'{self._booking_type_name}: {self.booked_item}\n' \
          f'Motif: {self._booking.motif}\n' \
          f'Veuillez valider ou refuser cette demande de réservation sur {reservation_url(self._booking)}.'
        return message

    @property
    def notification_subject(self) -> str:
        return  'Nouvelle réservation en attente de validation'

    @property
    def acknowledgement_text(self) -> str:
         return f"{self.default_text}\n\nVotre demande est en attente de validation.\n\n{reservation_url(self._booking)}"
    @property
    def acknowledgement_subject(self) -> str:
        return 'Votre demande de réservation a été effectuée'

    @property
    def cancellation_text(self) -> str:
        return f'La réservation suivante a été annulée :\n{self.default_text}'

    @property
    def cancellation_subject(self) -> str:
        return 'Annulation de votre réservation'


    @property
    def recipient(self):
        return self._booking.user.email

class RoomReservationTemplate(MessageTemplate):

    def __init__(self, booking):
        super().__init__(booking)
        self._booking_type_name = 'Salle'

    @property
    def booked_item(self) -> str:
        return self._booking.room_category
    @property
    def default_text(self) -> str:
        return f'Nombre de personnes: {self._booking.peopleAmount}\n{super().default_text}'

class EquipmentReservationTemplate(MessageTemplate):

    def __init__(self, booking):
        super().__init__(booking)
        self._booking_type_name = 'Équipement'

    @property
    def booked_item(self) -> str:
        return self._booking.equipment_category

    # CREATION DE RESERVATION
def send_reservation_confirmation_email_admin(bookingTemplate):
    """
    Envoie un mail qui confirme directement la réservation faite par l'admin
    """
    subject = bookingTemplate.confirmation_subject
    message = bookingTemplate.greeting + '\n\n' + bookingTemplate.confirmation_text

    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = [bookingTemplate.recipient] + settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list, fail_silently=False)


def send_request_validation_email_admin(bookingTemplate):
    """
    Envoie un mail qui demande la confirmation de la réservation d'un utilisateur
    """
    subject = bookingTemplate.notificaiton_subject
    message = bookingTemplate.notification_text

    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)

def send_reservation_acknowledgement_email_user(bookingTemplate):
    """
    Envoie un mail qui atteste de la demande réservation d'un utilisateur
    """
    subject = bookingTemplate.acknowledgement_subject
    message = f'{bookingTemplate.greeting_template}\n\n{bookingTemplate.acknowledgement_text}'
    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = [bookingTemplate.recipient]
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email_user(bookingTemplate):
    """
    Envoie un mail qui confirme l'annulation effectuée par l'utilisateur d'une réservation (en attente)
    """
    subject = bookingTemplate.cancellation_subject
    message = bookingTemplate.cancellation_text
    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = [bookingTemplate.recipient]
    send_mail(subject, message, sender, recipient_list)

