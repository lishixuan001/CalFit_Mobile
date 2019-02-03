from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Record(models.Model):
    def __str__(self):
        return "{username} : {date} : {steps}".format(username=self.user.username, date=self.date.date(), steps=self.steps)

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    steps = models.IntegerField(default=0)
    # date -> 20190101
    # Datetime ->  timezone.datetime(2019, 1, 30, 12, 30, 55, 000)
    date = models.DateTimeField(default=timezone.now(), blank=True)
