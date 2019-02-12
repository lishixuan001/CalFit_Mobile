from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Record(models.Model):
    def __str__(self):
        return "{username} : {date} : {steps}".format(username=self.user.username, date=self.date.date(), steps=self.steps)

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # date -> 20190101
    # Datetime ->  timezone.datetime(2019, 1, 30, 12, 30, 55, 000)
    # date => datetime.date() -> datetime.date(2019, 1, 30)
    # Record(user=user, steps=steps, date=timezone.datetime(2019, 1, 30).date())
    date = models.DateTimeField(default=timezone.now, blank=True)
    steps = models.IntegerField(default=0)

    def get_user(self):
        return self.user
    def get_date(self):
        return self.date
    def get_steps(self):
        return self.steps

class Goal(models.Model):
    def __str__(self):
        return "{username} : {date} : {goal}".format(username=self.user.username, date=self.date.date(), goal=self.goal)

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # date -> 20190101
    # Datetime ->  datetime = timezone.datetime(2019, 1, 30, 12, 30, 55, 000)
    # date => datetime.date() -> datetime.date(2019, 1, 30)
    # Record(user=user, steps=steps, date=timezone.datetime(2019, 1, 30).date())
    date = models.DateTimeField(default=None, blank=True)
    goal = models.IntegerField(default=0)

    def get_user(self):
        return self.user
    def get_date(self):
        return self.date
    def get_goal(self):
        return self.goal

class Message(models.Model):
    def __str__(self):
        return "[{title}] : [{content}]".format(title=self.message_title, content=self.message_content[:20])

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # date -> 20190101
    # Datetime ->  datetime = timezone.datetime(2019, 1, 30, 12, 30, 55, 000)
    # date => datetime.date() -> datetime.date(2019, 1, 30)
    # Record(user=user, steps=steps, date=timezone.datetime(2019, 1, 30).date())
    date = models.DateTimeField(default=None, blank=True)
    # type -> "plaintext"
    #      -> "interactive"
    type = models.IntegerField(default=0)
    responded = models.BooleanField(default=False)
    message_title = models.CharField(default=None, max_length=100)
    message_content = models.CharField(default=None, max_length=500)
    message_respond_yes = models.CharField(default=None, max_length=500)
    message_respond_no = models.CharField(default=None, max_length=500)


