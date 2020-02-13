from django.contrib import admin

from .models import Credential, Domain

admin.site.register(Credential)
admin.site.register(Domain)
