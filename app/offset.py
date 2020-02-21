from django.db import transaction
from django.utils import timezone

from app.models import Offset


def next_username_offset(client, now: timezone.datetime) -> Offset:
    return next_offset(client, now, 0)


def next_password_offset(client, now: timezone.datetime) -> Offset:
    return next_offset(client, now, 1)


@transaction.atomic
def next_offset(client, now: timezone.datetime, type=0) -> Offset:
    # dernier offset :
    # - non aquitté
    # - en timeout
    last_nack_timeouts = Offset.objects \
                             .filter(last_send__lt=(now - timezone.timedelta(minutes=15)), ack=False,
                                     type=type).order_by('id')[:1]

    if len(last_nack_timeouts) == 0:
        # pas de dernier offset non ack en timeout, il faut en créer un.
        last = Offset.objects.filter(type=type).order_by('-value')[:1]
        if len(last) == 0:
            offset = Offset(value=0, client=client, type=type, last_send=now)
        else:
            offset = Offset(value=last[0].value + 256, client=client, type=type, last_send=now)
        offset.save()
        return offset
    else:
        # on reprend le dernier offset qui est tombé en timeout.
        last_nack_timeout = last_nack_timeouts[0]
        last_nack_timeout.client = client
        last_nack_timeout.last_send = now
        last_nack_timeout.save()
        return last_nack_timeout


def ack(offset: Offset) -> None:
    offset.ack = True
    offset.save()
