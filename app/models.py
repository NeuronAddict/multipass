import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Domain(models.Model):
    name = models.CharField(max_length=200, unique=True)
    chunk_size = models.IntegerField(default=settings.DEFAULT_CHUNK_SIZE)
    url = models.CharField(max_length=4096, default='')
    username_offset = models.IntegerField(default=0)
    password_offset = models.IntegerField(default=0)


class Offset(models.Model):
    value = models.PositiveIntegerField()
    ack = models.BooleanField(default=False)
    last_send = models.DateTimeField(default=timezone.now)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)

    def values(self):
        raise NotImplementedError()


class Client(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    ip = models.GenericIPAddressField(unpack_ipv4=True)
    user_agent = models.CharField(max_length=400)
    current_offset = models.ForeignKey(Offset, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return "<Client: ip: {},user_agent: {}>"\
            .format(self.ip, self.user_agent)


class Username(models.Model):
    username = models.CharField(max_length=200, unique=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Password(models.Model):
    password = models.CharField(max_length=200, unique=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.password


class Credential(models.Model):
    username = models.CharField(max_length=400)
    password = models.CharField(max_length=400)
    found_date = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
