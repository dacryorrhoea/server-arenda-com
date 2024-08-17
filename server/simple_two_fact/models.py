from django.db import models

class ConfirmCode(models.Model):
    code = models.IntegerField()

    def __str__(self):
        return f'Код подтверждения №{self.id}'
