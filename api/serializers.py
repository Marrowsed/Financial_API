from rest_framework import serializers
from .models import *

class RevenueSerial(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = "__all__"

class ExpenseSerial(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"