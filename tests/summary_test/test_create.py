import json
import base64
from unittest import TestCase

import pytest
from django.db.models import Sum
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from datetime import datetime
from api.models import Revenue, Expense

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    """
    Test register
    """
    payload = {
        "username": "tester",
        "password": "T3st!ngFun",
        "password2": "T3st!ngFun",
        "email": "test@test.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    response = client.post('/register/', data=json.dumps(payload), content_type='application/json')

    assert response.status_code == 201


class RevenueTests(TestCase):
    """
    Revenue Tests
    """

    def setUp(self):
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        self.username = 'tester'
        self.email = 'test@test.com'
        self.password = 'T3st!ngFun'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )
        self.revenue = Revenue.objects.create(description="Test", value=5000, date=datetime.now(), user=self.user)
        self.expense = Expense.objects.create(description="iFood", category="Food", value=400, date=datetime.now(),
                                              user=self.user)
        self.expense2 = Expense.objects.create(description="Uber", category="Transport", value=40, date=datetime.now(),
                                               user=self.user)
        self.expense3 = Expense.objects.create(description="99", category="Transport", value=40, date=datetime.now(),
                                               user=self.user)

    @pytest.mark.django_db
    def test_get_summary(self):
        """
        Testing summary endpoint
        """
        credentials = ('%s:%s' % (self.username, self.password))
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        auth = 'Basic %s' % base64_credentials
        response = self.csrf_client.get(
            f'/summary/{datetime.now().year}/{datetime.now().month}/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_list_revenue(self):
        """
        Test calculate summary by year and month
        """
        credentials = ('%s:%s' % (self.username, self.password))
        base64_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        auth = 'Basic %s' % base64_credentials
        response = self.csrf_client.get(
            f'/summary/{datetime.now().year}/{datetime.now().month}/',
            HTTP_AUTHORIZATION=auth
        )
        data = response.data

        expense_total = self.expense.value + self.expense2.value + self.expense3.value
        final_value = self.revenue.value - expense_total
        category_expense = Expense.objects.filter(date__year=datetime.now().year, date__month=datetime.now().month,
                                                  user=self.user).values('category').annotate(Total_Value=Sum('value'))
        final_category = []
        final_sum = 0

        for i in category_expense:
            """Sum all the Total_Value"""
            final_sum += i['Total_Value']
        for c in category_expense:
            """Append in a list all the Values and %"""
            final_category.append(
                f"{c['category']}: ${c['Total_Value']} - {float(c['Total_Value'] / final_sum) * 100:.2f}%")



        assert response.status_code == 200
        assert data['Revenue/Month'] == f"${self.revenue.value}.0"
        assert data['Expense/Month'] == f"${expense_total}.0"
        assert data['Final Value'] == f"${final_value}.0"
        assert str(data['Category']) == str(final_category)

