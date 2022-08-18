from django.db.models import Sum
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import *


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet
    """
    queryset = User.objects.all()
    serializer_class = UserSerial


class RevenueViewSet(viewsets.ModelViewSet):
    """
    Revenue ViewSet filtered by user and can query by description
    """
    serializer_class = RevenueSerial
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description']

    def get_queryset(self):
        return Revenue.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RevenueYearMonthList(viewsets.ModelViewSet):
    """
    Revenue ViewSet with year/month and user filter
    """
    serializer_class = RevenueSerial

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Revenue.objects.filter(date__year=year, date__month=month, user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Expense ViewSet filtered by user and can query by description
    """
    serializer_class = ExpenseSerial
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseYearMonthList(viewsets.ModelViewSet):
    """
    Expense ViewSet with year/month and user filter
    """
    serializer_class = ExpenseSerial

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Expense.objects.filter(date__year=year, date__month=month, user=self.request.user)


class SummaryByMonthYear(APIView):
    """
    Summary View by user
    """
    queryset = Revenue.objects.none()

    def get(self, request, year, month):
        total_revenue = Revenue.objects.filter(date__year=year, date__month=month, user=self.request.user).aggregate(
            Sum('value'))['value__sum'] or 0
        total_expense = Expense.objects.filter(date__year=year, date__month=month, user=self.request.user).aggregate(
            Sum('value'))['value__sum'] or 0
        category_expense = Expense.objects.filter(date__year=year, date__month=month, user=self.request.user).values(
            'category').annotate(
            Total_Value=Sum('value'))
        final_category = []
        final_sum = 0

        for i in category_expense:
            """Sum all the Total_Value"""
            final_sum += i['Total_Value']
        for c in category_expense:
            """Append in a list all the Values and %"""
            final_category.append(
                f"{c['category']}: ${c['Total_Value']} - {float(c['Total_Value'] / final_sum) * 100:.2f}%")

        final_value = total_revenue - total_expense

        return Response({
            'Revenue/Month': f"${total_revenue}",
            'Expense/Month': f"${total_expense}",
            'Final Value': f"${final_value}",
            "Category": final_category
        })


class RegisterUserView(generics.CreateAPIView):
    """
    Register User View
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerial
