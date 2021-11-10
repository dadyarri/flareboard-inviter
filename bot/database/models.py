from tortoise import fields, Model


class InviteCode(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=64)
    activated_by = fields.BigIntField(null=True)
