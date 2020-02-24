import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    cred_json = json.loads(request.body)
    if cred_json['username'] == 'ansible' and cred_json['password'] == 'yankees':
        return HttpResponse(status=301)
    else:
        return HttpResponse(status=401)
