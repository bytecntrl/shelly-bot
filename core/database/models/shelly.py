from tortoise import fields
from tortoise.models import Model


class Shelly(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(500, unique=True)

    class Meta:
        table = "shelly"
