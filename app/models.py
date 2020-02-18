from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=200)
    usernames_dict = models.CharField(max_length=200, default='')
    passwords_dict = models.CharField(max_length=200, default='')
    chunk_size = models.IntegerField(default=256)
    url = models.CharField(max_length=4096, default='')


class Credential(models.Model):
    username = models.CharField(max_length=400)
    password = models.CharField(max_length=400)
    found_date = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
