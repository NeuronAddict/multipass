from datetime import datetime, timedelta

from app.models import Offset


class OffsetUtils:

    @classmethod
    def next_username_offset(cls, client, now: datetime) -> Offset:
        last = Offset.objects.filter(last_send__gt=(now - timedelta(minutes=15)), ack=False).order_by('id')[:1]

        if len(last) == 0:
            offset = Offset(value=0, client=client, type=0)
        else:
            offset = Offset(value=last.value+256, client=client, type=0)

        offset.save()
        return offset
