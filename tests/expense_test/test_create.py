import json
import base64
from unittest import TestCase

import pytest
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from datetime import datetime
from api.models import Expense

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


class ExpenseTests(TestCase):
    """
    Expense Tests
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
        print(self.user)
        self.expense = Expense.objects.create(description="Test", value=100, category="Other", date=datetime.now(), user=self.user)

    @pytest.mark.django_db
    def test_get_list_expense(self):
        """
        Test to return a list
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.get(
            '/expense/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_expense_detail(self):
        """
        Test to return a detail registry
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.get(
            f'/expense/{self.expense.id}/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_expense_description(self):
        """
        Test to return a registry description
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.get(
            f'/expense/?description={self.expense.description}/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_list_expense_year_month(self):
        """
        Test to return a list with year and month filter
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.get(
            f'/expense/{datetime.now().year}/{datetime.now().month}/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_expense_detail(self):
        """
        Test to delete a detail registry
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.delete(
            f'/expense/{self.expense.id}/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_post_expense(self):
        """
        Test to POST a registry
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.post(
            '/expense/',
            {'description': 'Test', 'value': 1, 'category': 'Food', 'date': '2022-01-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_expense_without_category(self):
        """
        Test to POST a registry
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.post(
            '/expense/',
            {'description': 'Test', 'value': 1, 'date': '2022-01-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_same_description_different_month(self):
        """
        Test to create the same registry with same description in another month
        """
        month = int(datetime.now().month) + 1
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        self.csrf_client.post(
            f'/expense/',
            {'description': 'Test', 'value': 1, 'category': 'Food', 'date': f'{datetime.now().year}-{month:02}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        response = self.csrf_client.post(
            f'/expense/',
            {'description': 'Test', 'value': 1, 'category': 'Food', 'date': f'{datetime.now().year}-{datetime.now().month:02}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_same_description_different_year(self):
        """
        Test to create the same registry with same description in another month
        """
        year = int(datetime.now().year) + 1
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        self.csrf_client.post(
            f'/expense/',
            {'description': 'Test', 'value': 1, 'category': 'Transport', 'date': f'{year}-{datetime.now().month}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        response = self.csrf_client.post(
            f'/revenue/',
            {'description': 'Test', 'value': 1, 'category': 'Transport', 'date': f'{datetime.now().year}-{datetime.now().month:02}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_fail_delete_expense_detail_twice(self):
        """
        Test to delete a detail registry twice
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        self.csrf_client.delete(
            f'/expense/{self.expense.id}/',
            HTTP_AUTHORIZATION=auth
        )
        response = self.csrf_client.delete(
            f'/expense/{self.expense.id}/',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 404 #Not found

    @pytest.mark.django_db
    def test_fail_expense_without_description(self):
        """
        Test fail registry without description
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.post(
            '/expense/',
            {'description': '', 'value': 1, 'category': 'Food', 'date': '2022-01-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_fail_expense_without_value(self):
        """
        Test fail registry without value
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.post(
            '/expense/',
            {'description': 'Test', 'value': "", 'category': 'Food', 'date': '2022-01-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_fail_expense_without_date(self):
        """
        Test fail registry without date
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.post(
            '/expense/',
            {'description': 'Test', 'value': 1, 'category': 'Food', 'date': ''},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_fail_expense_with_different_date_format(self):
        """
        Test fail registry with different date format
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        response = self.csrf_client.post(
            '/expense/',
            {'description': 'Test', 'value': 1, 'category': 'Food', 'date': '01-01-2022'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_fail_post_same_description_month(self):
        """
        Test to create the same registry with same description in another month
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        self.csrf_client.post(
            f'/revenue/',
            {'description': 'Test', 'value': 1, 'category': 'Transport', 'date': f'{datetime.now().year}-{datetime.now().month}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        response = self.csrf_client.post(
            f'/revenue/',
            {'description': 'Test', 'value': 1, 'category': 'Transport', 'date': f'{datetime.now().year}-{datetime.now().month}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_fail_post_case_insensitve(self):
        """
        Test to create the same registry case insensitive
        """
        bearer = self.csrf_client.post('/token/', data={'username': f'{self.username}', 'password': f'{self.password}'})
        token = bearer.data
        auth = f"Bearer {token['access']}"
        self.csrf_client.post(
            f'/revenue/',
            {'description': 'Test', 'value': 1, 'date': f'{datetime.now().year}-{datetime.now().month}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        response = self.csrf_client.post(
            f'/revenue/',
            {'description': 'test', 'value': 1, 'category': 'Other', 'date': f'{datetime.now().year}-{datetime.now().month}-01'},
            format='json',
            HTTP_AUTHORIZATION=auth
        )
        assert response.status_code == 400