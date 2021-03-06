from django import forms
from django.db.models import fields
from django.db.models.fields import CharField

from . import models

class find(forms.Form):
    name = forms.CharField(label='Your name', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'username'}))

class createakun(forms.ModelForm):
    class Meta:
        model = models.Accounts
        fields = [
            'id_customer',
            'type',
            'balance',
        ]
    # id_customer = forms.CharField(max_length=20)
    # tipe = [('saving','saving'),('loan','loan'),('checking account','checking account')]
    # type = forms.CharField(max_length=30,choices=tipe,default='saving')
    # balance = forms.IntegerField()

class createnasabah(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = [
            'name',
            'address',
            'phone',
            'email',
        ]

class transaksi(forms.Form):
    id_account = forms.CharField(max_length=20)
    type = forms.CharField(max_length=20)
    amount = forms.IntegerField()

    #only for loan
    id_pinjam = forms.CharField(max_length=30, required=False)