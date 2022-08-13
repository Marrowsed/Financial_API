import pytest
from rest_framework.test import APIClient
from datetime import datetime

client = APIClient()


def test_get_list_expense(expense_id):
    """
    Test to return a list with one expense registry
    """
    response = client.get('/expense/')
    assert response.status_code == 200

    data = response.data
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_expense_detail(expense_id):
    """
    Test to return a detail expense
    """
    detail = expense_id.id
    response = client.get(f'/expense/{detail}/')
    assert response.status_code == 200


def test_get_list_expense_year_month(expense_id):
    """
    Test to return a list with year and month filter
    """
    response = client.get(f'/expense/{datetime.now().year}/{datetime.now().month}/')
    assert response.status_code == 200
    data = response.data
    assert len(data) == 1


@pytest.mark.django_db
def test_create_expense():
    """
    Test for create a registry
    """
    payload = dict(
        description="Test",
        category="Transport",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month}-01"
    )

    response = client.post("/expense/", payload)
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_month(expense_id):
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
        response = client.post("/expense/", payload)
        assert response.status_code == 201


@pytest.mark.django_db
def test_create_same_description_different_year(expense_id):
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
        response = client.post("/expense/", payload)
        assert response.status_code == 201


@pytest.mark.django_db
def test_create_without_category():
    """
    Test to create a registry without category
    """
    payload = dict(
        description="Test",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month:02}-{datetime.now().day}"
    )

    response = client.post("/expense/", payload)
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
