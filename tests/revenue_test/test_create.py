import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_create_revenue():
    payload = dict(
        description="Test",
        value=100,
        date="2022-08-12"
    )

    response = client.post("/revenue/", payload)
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_month():
    first = dict(
        description="Test",
        value=100,
        date="2022-08-12"
    )
    client.post("/revenue/", first)
    payload = dict(
        description="Test",
        value=100,
        date="2022-09-12"
    )

    response = client.post("/revenue/", payload)
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_year(capsys):
    first = dict(
        description="Test",
        value=100,
        date="2022-08-12"
    )
    client.post("/revenue/", first)
    payload = dict(
        description="Test",
        value=100,
        date="2023-08-12"
    )

    response = client.post("/revenue/", payload)

    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_get_endpoint():

    response = client.get("/revenue/")

    assert response.status_code == 200
