from django.contrib import admin
from .models import Accounts,Accounttransactions,Customers
# Register your models here.

admin.site.site_header = 'Bank Management Admin DASHBOARD'

"SELECT id_customer, name FROM customer"
class CustomersTable(admin.ModelAdmin):
    list_display = ["id_customer","name",]
    

admin.site.register((Accounts,Accounttransactions))
admin.site.register(Customers,CustomersTable)