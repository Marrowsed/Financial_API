from django.db import models


# Create your models here.

class Revenue(models.Model):
    description = models.CharField(max_length=200, unique_for_month="date")
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.value} - {self.date}"

    def save(self, *args, **kwargs):
        r = Revenue.objects.filter(date__month=self.date.month, date__year=self.date.year, description=self.description)
        if r.exists():
            r.description = self.description
            r.value = self.value
            r.date = self.date
        else:
            return False
        super(Revenue, self).save(*args, **kwargs)


class Expense(models.Model):
    description = models.CharField(max_length=200, unique_for_month="date")
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.value} - {self.date}"

    def save(self, *args, **kwargs):
        e = Expense.objects.filter(date__month=self.date.month, date__year=self.date.year, description=self.description)
        if e.exists():
            e.description = self.description
            e.value = self.value
            e.date = self.date
        else:
            return False
        super(Expense, self).save(*args, **kwargs)
