from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(Revenue)
admin.site.register(Expense)