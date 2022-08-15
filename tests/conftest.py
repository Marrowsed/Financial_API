import pytest, json
from api.models import Revenue, Expense
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from datetime import datetime

client = APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create(
        username='tester',
        email='test@m.com',
        first_name='Firstname',
        last_name='Lastname'
    )
    user.set_password('T3st!ngFun')
    user.save()
    return user

@pytest.fixture
def auth_client():
    payload = {
        "username": "tester",
        "password": "T3st!ngFun",
        "password2": "T3st!ngFun",
        "email": "test@gmail.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    client.post('/register/', data=json.dumps(payload), content_type='application/json')
    return client

@pytest.fixture
def revenue_id(db, test_user):
    return Revenue.objects.create(description="Test", value=100, date=datetime.now(), user=test_user)

@pytest.fixture
def expense_id(db):
    return Expense.objects.create(description="Test", category="Other", value=100, date=datetime.now(), user=test_user)