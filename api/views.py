from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from api.models import *
from api.serializers import *


# Create your views here.

@api_view(['GET'])
def api_webhook(request, format=None):
    """
    API Webhook
    """
    return Response({
        'revenue': reverse('revenue-list', request=request, format=format),
        'expense': reverse('expense-list', request=request, format=format)
    })


class RevenueViewSet(viewsets.ModelViewSet):
    """
    Revenue ViewSet with description filter
    """
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerial
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description']


class RevenueYearMonthList(viewsets.ModelViewSet):
    serializer_class = RevenueSerial

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Revenue.objects.filter(date__year=year, date__month=month)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Expense ViewSet with description filter
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerial
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description']


class ExpenseYearMonthList(viewsets.ModelViewSet):
    serializer_class = ExpenseSerial

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Expense.objects.filter(date__year=year, date__month=month)


class SummaryByMonthYear(APIView):
    queryset = Revenue.objects.none()

    def get(self, request, year, month):
        total_revenue = Revenue.objects.filter(date__year=year, date__month=month).aggregate(
            Sum('value'))['value__sum'] or 0
        total_expense = Expense.objects.filter(date__year=year, date__month=month).aggregate(
            Sum('value'))['value__sum'] or 0
        category_expense = Expense.objects.filter(date__year=year, date__month=month).values('category').annotate(Total_Value=Sum('value'))
        final_value = total_revenue - total_expense

        return Response({
            'Receita/Mês': f"R${total_revenue}",
            'Despesa/Mês': f"R${total_expense}",
            'Saldo Final/Mês': f"R${final_value}",
            "Categorias": category_expense
        })
