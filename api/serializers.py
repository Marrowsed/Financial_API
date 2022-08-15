from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import *


class RevenueSerial(serializers.ModelSerializer):
    """
    Revenue Serializer for all
    """

    class Meta:
        model = Revenue
        fields = ['description', 'value', 'date']


class ExpenseSerial(serializers.ModelSerializer):
    """
    Expense Serializer for all
    """

    class Meta:
        model = Expense
        fields = ['description', 'category', 'value', 'date']


class UserSerial(serializers.ModelSerializer):
    """
    User Serializer for all
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RegisterUserSerial(serializers.ModelSerializer):
    """
    Register User Serializer
    """
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password doesn't match !"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
