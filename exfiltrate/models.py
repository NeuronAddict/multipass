from django.db import models


class Credential(models.Model):
    username = models.CharField(max_length=400)
    password = models.CharField(max_length=400)
    found_data = models.DateTimeField(auto_now=True)

