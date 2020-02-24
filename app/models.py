import uuid

from django.conf import settings
from django.db import models, connection
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
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT username,password FROM app_password, app_username ORDER BY app_password.id, app_username.id LIMIT %s OFFSET %s',
                [self.domain.chunk_size, self.value])
            while True:
                res = cursor.fetchone()
                if res is None:
                    break
                yield {'username': res[0], 'password': res[1]}


class Client(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, null=True)
    ip = models.GenericIPAddressField(unpack_ipv4=True)
    user_agent = models.CharField(max_length=400, null=True)
    current_offset = models.ForeignKey(Offset, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return "<Client {}: uuid={}, ip: {},user_agent: {}, current_offset: {}>" \
            .format(self.id, self.uuid, self.ip, self.user_agent, self.current_offset)


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
