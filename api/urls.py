from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from .views import *

revenue_list = RevenueViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

revenue_detail = RevenueViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

revenue_year_month = RevenueYearMonthList.as_view({
    'get': 'list'
})

expense_list = ExpenseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

expense_detail = ExpenseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

expense_year_month = ExpenseViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path('', views.api_webhook),
    path('revenue/', revenue_list, name='revenue-list'),
    path('revenue/<int:pk>/', revenue_detail, name='revenue-detail'),
    path('revenue/<int:year>/<int:month>/', revenue_year_month, name='revenue-year-month'),
    path('expense/', expense_list, name='expense-list'),
    path('expense/<int:pk>/', expense_detail, name='expense-detail'),
    path('expense/<int:year>/<int:month>/', expense_year_month, name='expense-year-month'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
