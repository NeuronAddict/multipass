import logging

from app.models import Client

logger = logging.getLogger('app.client')


def get_client(request, uuid):
    """
    Get a client or create if not exists
    :param request:
    :param uuid:
    :return:
    """
    if Client.objects.filter(uuid=uuid).exists():
        return Client.objects.get(uuid=uuid)
    else:
        client = Client(uuid=uuid, ip=get_client_ip(request), user_agent=request.headers['User-Agent'])
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
