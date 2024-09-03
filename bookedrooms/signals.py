from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from bookedrooms.models import BookedRoom
from users.models import CustomUser


@receiver(post_save, sender=BookedRoom)
def send_email(sender, instance, created=False, **kwargs):
    print(f'post_save trigger for {instance.pk}')
    if created:
        print('Creation')

    print(instance.status)
    print(instance.user)
    print(type(instance.user))
    print(instance.user.email)
    print(vars(instance.user))

@receiver(pre_delete, sender=BookedRoom)
def send_email(sender, instance, **kwargs):
    print(f'pre_delete trigger for {instance.pk}')

@receiver(post_delete, sender=BookedRoom)
def send_email(sender, instance, **kwargs):
    print(f'post_delete trigger for {instance.pk}')
