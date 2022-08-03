from django.db import models


# Create your models here.

def revenue_filter_by_description(description):
    return Revenue.objects.filter(description=description).exists()


def revenue_filter_by_date(date):
    return Revenue.objects.filter(date=date).exists()


class Revenue(models.Model):
    description = models.CharField(max_length=200, blank=False)
    value = models.FloatField(blank=False)
    date = models.DateField(blank=False)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.date}"

    def save(self, *args, **kwargs):
        if revenue_filter_by_description(self.description) and revenue_filter_by_date(self.date):
            raise ValueError("Registro Duplicado !")
        elif not revenue_filter_by_description(self.description):  # Create/Update a registry
            super().save(*args, **kwargs)
        elif Revenue.objects.filter(date__month=self.date.month,
                                    date__year=self.date.year).exists() and not revenue_filter_by_description(
            self.description):  # Create/Update a Registry
            super().save(*args, **kwargs)
        elif revenue_filter_by_description(self.description) and not Revenue.objects.filter(
                description=self.description, date__year=self.date.year).exists():
            # Create the same registry in another month/year
            super().save(*args, **kwargs)
        elif revenue_filter_by_description(self.description) and not Revenue.objects.filter(
                description=self.description, date__month=self.date.month, date__year=self.date.year).exists():
            # Update the date of a registry
            super().save(*args, **kwargs)
        else:
            raise ValueError("Erro no Registro !")


def expense_filter_by_description(description):
    return Expense.objects.filter(description=description).exists()


def expense_filter_by_date(date):
    return Expense.objects.filter(date=date).exists()


class Expense(models.Model):
    description = models.CharField(max_length=200, blank=False)
    value = models.FloatField(blank=False)
    date = models.DateField(blank=False)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.date}"

    def save(self, *args, **kwargs):
        if expense_filter_by_description(self.description) and expense_filter_by_date(self.date):
            raise ValueError("Registro Duplicado !")
        elif not expense_filter_by_description(self.description):  # Create/Update a registry
            super().save(*args, **kwargs)
        elif Expense.objects.filter(date__month=self.date.month,
                                    date__year=self.date.year).exists() and not expense_filter_by_description(
            self.description):  # Create/Update a Registry
            super().save(*args, **kwargs)
        elif expense_filter_by_description(self.description) and not Expense.objects.filter(
                description=self.description, date__year=self.date.year).exists():
            # Create the same registry in another month/year
            super().save(*args, **kwargs)
        elif expense_filter_by_description(self.description) and not Expense.objects.filter(
                description=self.description, date__month=self.date.month, date__year=self.date.year).exists():
            # Update the date of a registry
            super().save(*args, **kwargs)
        else:
            raise ValueError("Erro no Registro !")
