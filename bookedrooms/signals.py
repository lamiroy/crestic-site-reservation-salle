from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from RoomQueSTIC import utils
from RoomQueSTIC.utils import RoomReservationTemplate
from bookedrooms.models import BookedRoom


@receiver(post_save, sender=BookedRoom)
def send_email(sender, instance, created=False, **kwargs):
    # print(f'post_save trigger for {instance.pk}')
    message_template = RoomReservationTemplate(instance)
    if created:
        if instance.status == 'pending':
            utils.send_reservation_acknowledgement_email_user(message_template)
            utils.send_request_validation_email_admin(message_template)
    else:
        if instance.status == 'canceled':
            utils.send_reservation_cancellation_email_user(message_template)
        elif instance.status == 'validated':
            utils.send_reservation_confirmation_email_admin(message_template)
            pass

@receiver(pre_delete, sender=BookedRoom)
def send_email(sender, instance, **kwargs):
    # print(f'pre_delete trigger for {instance.pk}')
    pass

@receiver(post_delete, sender=BookedRoom)
def send_email(sender, instance, **kwargs):
    # print(f'post_delete trigger for {instance.pk}')
    pass
