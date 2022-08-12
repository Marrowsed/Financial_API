import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_create_expense():
    payload = dict(
        description="Test",
        category="Transporte",
        value=100,
        date="2022-08-12"
    )

    response = client.post("/expense/", payload)
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_month():
    first = dict(
        description="Test",
        category="Transporte",
        value=100,
        date="2022-08-12"
    )
    client.post("/expense/", first)
    payload = dict(
        description="Test",
        category="Alimentação",
        value=100,
        date="2022-09-12"
    )

    response = client.post("/expense/", payload)
    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_create_same_description_different_year():
    first = dict(
        description="Test",
        category="Transporte",
        value=100,
        date="2022-08-12"
    )
    client.post("/expense/", first)
    payload = dict(
        description="Test",
        category="Educação",
        value=100,
        date="2023-08-12"
    )

    response = client.post("/expense/", payload)

    code = response.status_code
    assert code == 201


@pytest.mark.django_db
def test_get_endpoint():

    response = client.get("/expense/")

    assert response.status_code == 200
