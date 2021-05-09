from django import forms

from . import models

class find(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)

class createakun(forms.ModelForm):
    class Meta:
        model = models.Accounts
        fields = [
            'id_account',
            'id_customer',
            'type',
            'balance',
        ]

class transaksi(forms.ModelForm):
    class Meta:
        model = models.Accounttransactions
        fields = [
            'id_account',
            'date_time',
            'type',
            'amount',
        ]