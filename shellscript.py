import django
from django.utils import timezone
django.setup()

from calfit.models import *

print("User Objects: ")
for user in User.objects.all():
    print("---> {}".format(user))
print("\n")

print("Record Objects: ")
for record in Record.objects.all():
    print("---> {}".format(record))
print("\n")

print("Goal Objects: ")
for goal in Goal.objects.all():
    print("---> {}".format(goal))
print("\n")
