from django.db import models

# Create your models here.

class Accounts(models.Model):
    id_account = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey('Customers', models.DO_NOTHING, db_column='id_customer')
    tipe = [('saving','saving'),('loan','loan'),('checking account','checking account')]
    type = models.CharField(max_length=30,choices=tipe,default='saving')
    balance = models.IntegerField()

    def __str__(self):
        return f'{self.id_account} - {self.type} - {self.id_customer.name}'
    

    class Meta:
        # managed = False
        db_table = 'accounts'

class Accounttransactions(models.Model):
    id_account = models.ForeignKey(Accounts, models.DO_NOTHING, db_column='id_account')  
    date_time = models.DateField(auto_now_add=True, null=True)
    tipe = [('saving','saving'),('loan','loan'),('checking account','checking account')]
    type = models.CharField(max_length=30,choices=tipe,default='saving')
    amount = models.IntegerField()

    

    def __str__(self):
        return "{}".format(self.id_account)

    class Meta:
        # managed = False
        db_table = 'accounttransactions'

class Customers(models.Model):
    id_customer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=60)

    def __str__(self):
        return "{}".format(self.id_customer)
    

    class Meta:
        managed = False
        db_table = 'customers'