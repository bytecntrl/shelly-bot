from tortoise import fields
from tortoise.models import Model


class Admin(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(unique=True)

    class Meta:
        table = "admin"
