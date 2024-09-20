from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from RoomQueSTIC import mailtemplates
from RoomQueSTIC.mailtemplates import EquipmentReservationTemplate
from bookedequipments.models import BookedEquipment


@receiver(post_save, sender=BookedEquipment)
def send_email(sender, instance, created=False, **kwargs):
    print(f'post_save trigger for {instance.pk}')
    message_template = EquipmentReservationTemplate(instance)
    if created:
        if instance.status == 'pending':
            mailtemplates.send_reservation_acknowledgement_email_user(message_template)
            mailtemplates.send_request_validation_email_admin(message_template)
    else:
        if instance.status == 'canceled':
            mailtemplates.send_reservation_cancellation_email_user(message_template)
        elif instance.status == 'validated':
            mailtemplates.send_reservation_confirmation_email_admin(message_template)
            pass


@receiver(pre_delete, sender=BookedEquipment)
def send_email(sender, instance, **kwargs):
    print(f'pre_delete trigger for {instance.pk}')


@receiver(post_delete, sender=BookedEquipment)
def send_email(sender, instance, **kwargs):
    print(f'post_delete trigger for {instance.pk}')
