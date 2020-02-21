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


class Client(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    ip = models.GenericIPAddressField(unpack_ipv4=True)
    user_agent = models.CharField(max_length=400)

    def __str__(self):
        return "<Client: ip: {},user_agent: {}>"\
            .format(self.ip, self.user_agent)


class Offset(models.Model):
    value = models.PositiveIntegerField()
    type = models.type = models.PositiveSmallIntegerField(choices=[(1, 'password'), (0, 'username')])
    ack = models.BooleanField(default=False)
    last_send = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    def values(self):
        if self.type == 0:
            return Username.objects.filter(id__range=[self.value, self.value+256]).values('username')
        else:
            if self.type == 1:
                return Password.objects.filter(id__range=[self.value, self.value + 256]).values('password')
            raise Exception('Bad type for Offset {}: {}'.format(self, self.type))


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
