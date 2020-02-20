from datetime import datetime, timedelta

from app.models import Offset


class OffsetUtils:

    @classmethod
    def next_username_offset(cls, now: datetime) -> int:
        last = Offset.objects.filter(last_send__gt=(now - timedelta(minutes=15)), ack=False).order_by('id')[:1]

        if len(last) == 0:
            return 0
        return last[0].value
