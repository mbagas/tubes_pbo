from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View

# Create your views here.
# import module
from . import models
from .models import Accounts, Customers, Accounttransactions
from .form import find
from .form import createakun
from .form import transaksi

# inheritance dari class view
class Account(View):
    template_name = 'bank/transaksi.html'
    form = transaksi()
    mode = None
    context = {}

    # override method get dari parent class view
    def get(self, *args, **kwargs):
        print(kwargs['akun_id'])
        if self.mode == 'deposit':
           
            self.form = transaksi()
            self.context = {
                "page_title":"deposit",
                "tipe":"deposit",
                "id_akun":kwargs['akun_id'],
                "transaksi_form":self.form,
            }
        elif self.mode == 'withdraw':

            self.form = transaksi()
            self.context = {
                "page_title":"withdraw",
                "tipe":"withdraw",
                "id_akun":kwargs['akun_id'],
                "transaksi_form":self.form,
            }

        elif self.mode == 'BalanceEnquiry':
            data_transaksi = Accounttransactions.objects.filter(id_account=kwargs['akun_id'])
            self.template_name = 'bank/data_transaksi.html'
            self.context = {
                "page_title":"Balance Enquiry",
                "tipe":"BalanceEnquiry",
                "id_akun":kwargs['akun_id'],
                "data_transaksi":data_transaksi,
            }
        
        return render(self.request, self.template_name, self.context)
        
    # override methode post dari parent class view    
    def post(self, *args, **kwargs):

        self.form = transaksi(self.request.POST or None)
        
        if self.mode == 'deposit':
            if self.form.is_valid():
                new_transaksi = Accounttransactions(
                    id_account = Accounts.objects.get(id_account=self.form.cleaned_data['id_account']),
                    type = self.form.cleaned_data['type'],
                    amount = self.form.cleaned_data['amount'],
                )
                new_transaksi.save()
                id_akun = str(self.form.cleaned_data['id_account'])
                nabung = int(self.form.cleaned_data['amount'])
                akun = Accounts.objects.get(id_account=id_akun)
                akun.balance = akun.balance + nabung
                akun.save()
        elif self.mode == 'withdraw':
            if self.form.is_valid():
                
                new_transaksi = Accounttransactions(
                    id_account = Accounts.objects.get(id_account=self.form.cleaned_data['id_account']),
                    type = self.form.cleaned_data['type'],
                    amount = self.form.cleaned_data['amount'],
                )
                new_transaksi.save()
                id_akun = str(self.form.cleaned_data['id_account'])
                ambil = int(self.form.cleaned_data['amount'])
                akun = Accounts.objects.get(id_account=id_akun)
                akun.balance = akun.balance - ambil
                if akun.balance < 0:
                    akun.balance = 0
                akun.save()
        
        return redirect('index')

class SavingAccount(Accounts,View):
    def get():
        return

def index(request, customer=0):
    
    form = find()
    
    context = {
        'form': form,
    }

    return render(request,'bank/index.html',context)

def akun(request):
    form = find()
    nasabah = models.Customers.objects.get(name=request.POST['name'])
    if nasabah:
        accounts = models.Accounts.objects.filter(id_customer=nasabah.id_customer)
    else:
        accounts = models.Accounts.objects.filter(id_customer=0)
    context = {
        'Title':'customer',
        'heading':'customer',
        'accounts':accounts,
        'form': form,
        'nasabah':nasabah,
    }

    return render(request,'bank/account.html',context)

def tambahakun(request,nasabah_id):
    cek_nasabah = models.Customers.objects.get(id_customer=nasabah_id)
    akun_form = createakun(request.POST or None)

    if request.method == 'POST':
        if akun_form.is_valid():
            akun_form.save()
        
        return redirect('index')
    
    context = {
        "akun_form":akun_form,
        "nasabah":cek_nasabah,
    }

    return render(request,'bank/createakun.html',context)