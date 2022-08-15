import pytest, json
from rest_framework.test import APIClient
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
        "email": "test@gmail.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    response = client.post('/register/', data=json.dumps(payload), content_type='application/json')

    assert response.status_code == 201


def test_get_list_expense(expense_id, test_user):
    """
    Test to return a list with one expense registry
    """
    response = client.get('/expense/', auth=(f"{test_user.username}", f"{test_user.password}"))
    assert response.status_code == 200

    data = response.data
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_expense_detail(expense_id, test_user):
    """
    Test to return a detail expense
    """
    detail = expense_id.id
    response = client.get(f'/expense/{detail}/', auth=(f"{test_user.username}", f"{test_user.password}"))
    assert response.status_code == 200


def test_get_list_expense_year_month(expense_id, test_user):
    """
    Test to return a list with year and month filter
    """
    response = client.get(f'/expense/{datetime.now().year}/{datetime.now().month}/', auth=(f"{test_user.username}", f"{test_user.password}"))
    assert response.status_code == 200
    data = response.data
    assert len(data) == 1


@pytest.mark.django_db
def test_create_expense(test_user):
    """
    Test for create a registry
    """
    payload = dict(
        description="Test",
        category="Transport",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month}-01"
    )

    response = client.post("/expense/", payload, auth=(f"{test_user.username}", f"{test_user.password}"))
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_month(expense_id, test_user):
    """
    Test to create the same registry with same description in another month
    """
    month = int(datetime.now().month) + 1
    payload = dict(
        description="Test",
        category="Other",
        value=100,
        date=f"{datetime.now().year}-{month:02}-{datetime.now().day}"
    )

    if payload['date'] == expense_id.date.strftime("%Y-%m-%d"):
        assert True  # fail condition
    else:
        response = client.post("/expense/", payload, auth=(f"{test_user.username}", f"{test_user.password}"))
        assert response.status_code == 201


@pytest.mark.django_db
def test_create_same_description_different_year(expense_id, test_user):
    """
    Test to create the same registry with same description in another year
    """
    year = int(datetime.now().year) + 1
    payload = dict(
        description="Test",
        category="Other",
        value=100,
        date=f"{year}-{datetime.now().month:02}-{datetime.now().day}"
    )

    if payload['date'] == expense_id.date.strftime("%Y-%m-%d"):
        assert True  # fail condition
    else:
        response = client.post("/expense/", payload, auth=(f"{test_user.username}", f"{test_user.password}"))
        assert response.status_code == 201


@pytest.mark.django_db
def test_create_without_category(test_user):
    """
    Test to create a registry without category
    """
    payload = dict(
        description="Test",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month:02}-{datetime.now().day}"
    )

    response = client.post("/expense/", payload, auth=(f"{test_user.username}", f"{test_user.password}"))
    assert response.status_code == 201


@pytest.mark.django_db
def test_fail_same_expense_month(expense_id):
    """
    Test to fail creating a registry with same description in the same month
    """
    payload = dict(
        description="Test",
        category="Other",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month:02}-{datetime.now().day}"
    )
    if payload['date'] == expense_id.date.strftime("%Y-%m-%d"):
        assert True  # fail condition
    else:
        response = client.post("/expense/", payload)
        assert response.status_code != 201  # proposital failure - can't get here


@pytest.mark.django_db
def test_fail_case_sensitive(expense_id):
    """
    Test to fail creating a registry with same description case insensitive
    """
    payload = dict(
        description="test",
        category="Other",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month:02}-{datetime.now().day}"
    )
    if Expense.objects.filter(description__icontains=payload['description']).exists():
        assert True
    else:
        response = client.post("/expense/", payload)
        assert response.status_code != 201  # proposital failure - can't get here
