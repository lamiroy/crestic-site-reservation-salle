from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from bookedrooms.models import BookedRoom


@receiver(post_save, sender=BookedRoom)
def send_email(sender, **kwargs):
    print(f'post_save trigger for {sender.pk}')


@receiver(pre_delete, sender=BookedRoom)
def send_email(sender, **kwargs):
    print(f'pre_delete trigger for {sender.pk}')
