from django.db import models


# Create your models here.

class Revenue(models.Model):
    description = models.CharField(max_length=200, unique_for_month="date")
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.description


class Expense(models.Model):
    description = models.CharField(max_length=200, unique_for_month="date")
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return self.description
