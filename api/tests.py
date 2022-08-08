import datetime

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from api.models import Revenue, Expense


class RevenueTests(APITestCase):

    def setUp(self):
        self.revenue = Revenue.objects.create(
            description="Test", value=100, date=datetime.datetime.now()
        )
        self.expense = Expense.objects.create(
            description="Test", value=100, category="Alimentação", date=datetime.datetime.now()
        )

    def test_create_revenue(self):
        """
        Test for create a revenue
        """
        data = {'description': 'Test', 'value': 100, 'date': '2023-08-01'}
        response = self.client.post('/revenue/', data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_revenue_another_year(self):
        """
        Test for the same revenue, the same month but another year
        """
        data = {'description': 'Test', 'value': 100, 'date': '2024-08-01'}
        response = self.client.post('/revenue/', data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_revenue(self):
        """
        Test for get a list of revenues
        """
        response = self.client.get('/revenue/', format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_query_revenue(self):
        """
        Test for get a list of revenues with query
        """
        response = self.client.get('/revenue/?description=test', format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ExpenseTests(APITestCase):
    def test_create_expense(self):
        """
        Test for create an expense
        """
        data = {'description': 'Test', 'value': 100, 'date': '2022-08-01'}
        response = self.client.post('/expense/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().description, 'Test')

    def test_create_revenue_another_year(self):
        """
        Test for the same revenue, the same month but another year
        """
        data = {'description': 'Test', 'value': 100, 'date': '2024-08-01'}
        response = self.client.post('/revenue/', data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expense(self):
        """
        Test for get a list of expense
        """
        response = self.client.get('/expense/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_query_expense(self):
        """
        Test for get a list of revenues with query
        """
        response = self.client.get('/expense/?description=test', format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
