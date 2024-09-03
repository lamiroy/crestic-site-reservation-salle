#
# File: signals.py
#

import json

from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated, cas_user_logout


"""
@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    args = {}
    args.update(kwargs)
    print('''cas_user_authenticated_callback:
    user: %s
    created: %s
    attributes: %s
    ''' % (
        args.get('user'),
        args.get('created'),
        json.dumps(args.get('attributes'), sort_keys=True, indent=2)))
"""
