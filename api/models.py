from django.db import models
from rest_framework import serializers


# Create your models here.

def revenue_filter_by_description(description):
    return Revenue.objects.filter(description__icontains=description).exists()


class Revenue(models.Model):
    user = models.ForeignKey('auth.User', related_name='revenues', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=False)
    value = models.FloatField(blank=False)
    date = models.DateField(blank=False)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.date}"

    def save(self, *args, **kwargs):
        if Revenue.objects.filter(description__icontains=self.description, date__month=self.date.month, date__year=self.date.year, user=self.user):
            raise serializers.ValidationError("Duplicated !")
        else:
            super().save(*args, **kwargs)
        """GAMBIARRAS
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
        """


def expense_filter_by_description(description):
    return Expense.objects.filter(description__icontains=description).exists()


class Expense(models.Model):
    OUTRAS = "Other"
    ESCOLHAS = (
        ("Food", "Food"),
        ("Health", "Health"),
        ("Home", "Home"),
        ("Transport", "Transport"),
        ("School", "School"),
        ("Fun", "Fun"),
        ("Unexpected", "Unexpected"),
        ("Other", "Other")
    )
    user = models.ForeignKey('auth.User', related_name='expenses', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=False)
    category = models.CharField(max_length=200, blank=True, choices=ESCOLHAS, default=OUTRAS)
    value = models.FloatField(blank=False)
    date = models.DateField(blank=False)

    def __str__(self):
        return f"{self.description} - {self.category} - {self.value} - {self.date}"

    def save(self, *args, **kwargs):
        if Expense.objects.filter(description__icontains=self.description, date__year=self.date.year, date__month=self.date.month, category=self.category, user=self.user):
            raise serializers.ValidationError("Duplicated !")
        else:
            super().save(*args, **kwargs)
        if self.category is None:
            self.category = "Other"
        """GAMBIARRAS
        if Expense.objects.filter(description=self.description, date__year=self.date.year, date__month=self.date.month):
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
        """