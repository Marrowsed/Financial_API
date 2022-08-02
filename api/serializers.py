from rest_framework import serializers
from .models import *


class RevenueSerial(serializers.ModelSerializer):
    """
    Revenue Serializer for all
    """
    class Meta:
        model = Revenue
        fields = "__all__"


class ExpenseSerial(serializers.ModelSerializer):
    """
    Expense Serializer for all
    """
    class Meta:
        model = Expense
        fields = "__all__"
