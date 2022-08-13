import pytest
from rest_framework.test import APIClient
from datetime import datetime

client = APIClient()


def test_get_list_expense(revenue_id):
    """
    Test to return a list with one revenue registry
    """
    response = client.get('/revenue/')
    assert response.status_code == 200

    data = response.data
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_expense_detail(revenue_id):
    """
    Test to return a detail revenue
    """
    detail = revenue_id.id
    response = client.get(f'/revenue/{detail}/')
    assert response.status_code == 200


def test_get_list_revenue_year_month(revenue_id):
    """
    Test to return a list with year and month filter
    """
    response = client.get(f'/revenue/{datetime.now().year}/{datetime.now().month}/')
    assert response.status_code == 200
    data = response.data
    assert len(data) == 1


@pytest.mark.django_db
def test_create_revenue():
    """
    Test for create a registry
    """
    payload = dict(
        description="Test",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month}-01"
    )

    response = client.post("/revenue/", payload)
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_month(revenue_id):
    """
    Test to create the same registry with same description in another month
    """
    month = int(datetime.now().month) + 1
    payload = dict(
        description="Test",
        value=100,
        date=f"{datetime.now().year}-{month:02}-{datetime.now().day}"
    )

    if payload['date'] == revenue_id.date.strftime("%Y-%m-%d"):
        assert True  # fail condition
    else:
        response = client.post("/revenue/", payload)
        assert response.status_code == 201


@pytest.mark.django_db
def test_create_same_description_different_year(revenue_id):
    """
    Test to create the same registry with same description in another year
    """
    year = int(datetime.now().year) + 1
    payload = dict(
        description="Test",
        value=100,
        date=f"{year}-{datetime.now().month:02}-{datetime.now().day}"
    )

    if payload['date'] == revenue_id.date.strftime("%Y-%m-%d"):
        assert True  # fail condition
    else:
        response = client.post("/revenue/", payload)
        assert response.status_code == 201


@pytest.mark.django_db
def test_fail_same_revenue_month(revenue_id):
    """
    Test to fail creating a registry with same description in the same month
    """
    payload = dict(
        description="Test",
        value=100,
        date=f"{datetime.now().year}-{datetime.now().month:02}-{datetime.now().day}"
    )
    if payload['date'] == revenue_id.date.strftime("%Y-%m-%d"):
        assert True  # fail condition
    else:
        response = client.post("/revenue/", payload)
        assert response.status_code != 201  # proposital failure - can't get here
