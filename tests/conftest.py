import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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