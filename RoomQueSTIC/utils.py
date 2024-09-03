from django.core.mail import send_mail  # Importe la fonctionnalité d'envoi de courrier électronique Django
from RoomQueSTIC import settings  # Importe les paramètres de configuration de l'application

def reservation_url(booked_room) -> str:
    return f'https://crestic.univ-reims.fr/reservations/roombooking/{booked_room.id}/edit/'

def greeting_template(booked_room) -> str:
    return f'Bonjour {booked_room.user.first_name},'

def text_template(booked_room) -> str:
    text = f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n'
    return text

# CREATION DE RESERVATION
def send_reservation_confirmation_email_admin(booked_room):
    """
    Envoie un mail qui confirme directement la réservation faite par l'admin
    """
    subject = 'Votre réservation a bien été validée'
    message = text_template(booked_room) + '\n\n' + 'https://crestic.univ-reims.fr/reservations'

    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booked_room.user.email] + settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list, fail_silently=False)


def send_request_validation_email_admin(booked_room):
    """
    Envoie un mail qui demande la confirmation de la réservation d'un utilisateur
    """
    subject = 'Nouvelle réservation en attente de validation'
    message = f'Une nouvelle réservation a été faite par {booked_room.user.first_name}' \
              f' {booked_room.user.last_name} ({booked_room.user.email}).\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez valider ou refuser cette demande de réservation sur {reservation_url(booked_room)}.'
    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)

def send_reservation_acknowledgement_email_user(booked_room):
    """
    Envoie un mail qui atteste de la demande réservation d'un utilisateur
    """
    subject = 'Votre demande de réservation a été effectuée'
    message = greeting_template(booked_room) + '\n\n' + text_template(booked_room) + f"\n\nVotre demande est en attente de validation.\n\n" + reservation_url(booked_room)
    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booked_room.user.email]
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email_user(booked_room):
    """
    Envoie un mail qui confirme l'annulation effectuée par l'utilisateur d'une réservation (en attente)
    """
    subject = 'Annulation de votre réservation'
    message = f'La réservation suivante a été annulée :\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n'
    sender = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booked_room.user.email]
    send_mail(subject, message, sender, recipient_list)

