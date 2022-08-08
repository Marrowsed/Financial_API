from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
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




class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Expense ViewSet with description filter
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerial
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description']


