from django.conf import settings
from django.db import transaction
from django.utils import timezone

from app.models import Offset, Client, Domain


def next_username_offset(domain: Domain, client: Client, now: timezone.datetime) -> Offset:
    return next_offset(domain, client, now, 0)


def next_password_offset(domain: Domain, client, now: timezone.datetime) -> Offset:
    return next_offset(domain, client, now, 1)


@transaction.atomic
def next_offset(domain: Domain, client, now: timezone.datetime, type=0) -> Offset:
    # dernier offset :
    # - non aquitté
    # - en timeout

    if client.current_offset is not None:
        return client.current_offset

    last_nack_timeouts = Offset.objects.filter(last_send__lt=(now - timezone.timedelta(minutes=15)), ack=False) \
                             .order_by('id')[:1]

    if len(last_nack_timeouts) == 0:
        # pas de dernier offset non ack en timeout, il faut en créer un.
        last = Offset.objects.order_by('-value')[:1]
        if len(last) == 0:
            offset = Offset(value=0, domain=domain, last_send=now)

        else:
            offset = Offset(value=last[0].value + domain.chunk_size, domain=domain, last_send=now)
        offset.save()
        client.current_offset = offset
        client.save()
        return offset
    else:
        # on reprend le dernier offset qui est tombé en timeout.
        last_nack_timeout = last_nack_timeouts[0]
        last_nack_timeout.client = client
        last_nack_timeout.last_send = now
        last_nack_timeout.save()
        client.current_offset = last_nack_timeout
        client.save()
        return last_nack_timeout


@transaction.atomic
def ack(client: Client) -> None:
    client.current_offset.ack = True
    client.current_offset.save()
    client.current_offset = None
    client.save()
