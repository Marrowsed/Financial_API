"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from api import views

schema_view = get_schema_view(
   openapi.Info(
      title="Financial API",
      default_version='v1',
      description="An API made to control your daily Revenue and Expenses. You can see your month summary and how much you spent in each category.",
      terms_of_service="#",
      contact=openapi.Contact(email="m4rr0ws@duck.com"),
      license=openapi.License(name="MRW License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'revenue', views.RevenueViewSet, basename='revenue'),
router.register(r'expense', views.ExpenseViewSet, basename='expense'),
router.register(r'user', views.UserViewSet, basename='expense'),

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('pannel/', admin.site.urls),
    path('', include(router.urls)),
    path(r'doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(r'token/', TokenObtainPairView.as_view(), name='register-token'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path(r'token/verify/', TokenVerifyView.as_view(), name='verify-token'),
    path(r'revenue/<int:year>/<int:month>/', views.RevenueYearMonthList.as_view({'get': 'list'}), name='revenue-year-month'),
    path(r'expense/<int:year>/<int:month>/', views.ExpenseYearMonthList.as_view({'get': 'list'}), name='expense-year-month'),
    path(r'summary/<int:year>/<int:month>/', views.SummaryByMonthYear.as_view(), name="summary-year-month"),
    path(r'register/', views.RegisterUserView.as_view(), name="register-user")
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
