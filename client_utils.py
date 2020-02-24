import logging

from django.db import transaction

from app.models import Client

logger = logging.getLogger('app.client')


@transaction.atomic
def get_client(request):
    """
    Get a client or create if not exists
    :param request:
    :return:
    """
    uuid = request.headers.get('X-CLIENT-UUID')
    client_ip = get_client_ip(request)
    user_agent = request.headers.get('User-Agent')

    if uuid and Client.objects.filter(uuid=uuid, uuid__isnull=False).exists():
        return Client.objects.get(uuid=uuid, uuid__isnull=False)
    else:
        if Client.objects.filter(uuid__isnull=True, ip=client_ip, user_agent=user_agent).exists():
            return Client.objects.get(uuid__isnull=True, ip=client_ip, user_agent=user_agent)
        else:
            client = Client(uuid=uuid, ip=client_ip, user_agent=user_agent)
            client.save()
            logger.info('[+] new client : {}'.format(client))
            return client


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
