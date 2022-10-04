from email.policy import default
from django.db import models


class Bitcoin(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
