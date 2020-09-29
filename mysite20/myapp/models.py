from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    # The max_length is the required argument for the CharField
    name = models.CharField(max_length=200)


class Course(models.Model):
    title = models.CharField(max_length=200)
    # Here we are defining a Many-to-One relationship from Course to Topic i.e: a topic can have many courses
    # The ForeignKey requires two argument: first the class to which the model is related and the on_delete option
    # The related_name name is used to access the many field in this case it's courses
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
