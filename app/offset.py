from django.db import transaction
from django.utils import timezone

from app.models import Offset


class OffsetUtils:

    @classmethod
    @transaction.atomic
    def next_username_offset(cls, client, now: timezone.datetime) -> Offset:
        # dernier offset :
        # - non aquitté
        # - en timeout
        last_nack_timeouts = Offset.objects \
                                 .filter(last_send__lt=(now - timezone.timedelta(minutes=15)), ack=False,
                                         type=0).order_by('id')[:1]

        if len(last_nack_timeouts) == 0:
            # pas de dernier offset non ack en timeout, il faut en créer un.
            last = Offset.objects.filter(type=0).order_by('-value')[:1]
            if len(last) == 0:
                offset = Offset(value=0, client=client, type=0, last_send=now)
            else:
                offset = Offset(value=last[0].value + 256, client=client, type=0, last_send=now)
            offset.save()
            return offset
        else:
            # on reprend le dernier offset qui est tombé en timeout.
            last_nack_timeout = last_nack_timeouts[0]
            last_nack_timeout.client = client
            last_nack_timeout.last_send = now
            last_nack_timeout.save()
            return last_nack_timeout
