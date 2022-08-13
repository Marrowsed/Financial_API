import pytest
from api.models import Revenue, Expense
from datetime import datetime


@pytest.fixture
def revenue_id(db):
    return Revenue.objects.create(description="Test", value=100, date=datetime.now())

@pytest.fixture
def expense_id(db):
    return Expense.objects.create(description="Test", category="Other", value=100, date=datetime.now())
