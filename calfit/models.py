from django.db import models
from django.contrib.auth.models import User
import time

class Record(models.Model):
    def __str__(self):
        return "{username}:{date}".format(self.user.username, self.date)

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = time.strftime("%Y%m%d")