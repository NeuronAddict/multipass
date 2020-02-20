from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=200, unique=True)
    chunk_size = models.IntegerField(default=256)
    url = models.CharField(max_length=4096, default='')
    username_offset = models.IntegerField(default=0)
    password_offset = models.IntegerField(default=0)


class Username(models.Model):
    username = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Password(models.Model):
    password = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)


class Credential(models.Model):
    username = models.CharField(max_length=400)
    password = models.CharField(max_length=400)
    found_date = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
