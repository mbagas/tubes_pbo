from django.contrib import admin
from .models import Accounts,Accounttransactions,Customers
# Register your models here.

admin.site.register((Accounts,Accounttransactions,Customers))