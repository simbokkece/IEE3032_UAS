from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.name)

class Actuator(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)