from email.policy import default
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100, default=1234)

    def __str__(self):
        return str(self.id)
