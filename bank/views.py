from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
# import module
from . import models
from .models import Accounts, Customers, Accounttransactions
from .form import createnasabah, find
from .form import createakun
from .form import transaksi

# ===================================
# === inheritance dari class view ===
# === untuk transaksi dasar akun ===
# ===================================
class Account(View):
    template_name = 'bank/transaksi.html'
    form = transaksi()
    mode = None
    context = {}

    # ===================================
    # === override method get dari parent class view ===
    # ===================================
    def get(self, *args, **kwargs):
        print(kwargs['akun_id'])
        data_akun = Accounts.objects.get(id_account=kwargs['akun_id'])
        if self.mode == 'deposit':
           
            self.form = transaksi()
            self.context = {
                "page_title":"deposit",
                "tipe":"deposit",
                "id_akun":data_akun.id_account,
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
            data_akun = Accounts.objects.get(id_account=kwargs['akun_id'])
            self.template_name = 'bank/data_transaksi.html'
            self.context = {
                "page_title":"Balance Enquiry",
                "tipe":data_akun.type,
                "id_akun":kwargs['akun_id'],
                "data_transaksi":data_transaksi,
            }
        
        return render(self.request, self.template_name, self.context)
    
    # ===================================
    # === override methode post dari parent class view ===    
    # ===================================
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
# ===============================================
# === inheritance dari class Account dan view ===
# ===============================================
class CheckingAccount(Accounts,View):
    mode = None
    def post(self, *args, **kwargs):
        return

# ===============================================
# === inheritance dari class Account dan view ===
# === untuk nambah pinjaman ===
# ===============================================
class LoanAccount(Account,View):
    template_name = 'bank/transaksi.html'
    form = transaksi()
    mode = None
    context = {}
   
   # === override method get dari parent class view ===
    def get(self, *args, **kwargs):
        print(kwargs)
        self.form = transaksi()
        self.context = {
            "page_title":"Loan",
            "tipe":"loan",
            "id_akun":kwargs['akun_id'],
            "transaksi_form":self.form,
        }
        return render(self.request, self.template_name, self.context)

    # === override methode post dari parent class view ===  
    def post(self, *args, **kwargs):
        self.form = transaksi(self.request.POST or None)

        if self.form.is_valid():
            new_transaksi = Accounttransactions(
                id_account = Accounts.objects.get(id_account=self.form.cleaned_data['id_account']),
                type = self.form.cleaned_data['type'],
                amount = self.form.cleaned_data['amount'],
            )
            new_transaksi.save()
            id_akun = str(self.form.cleaned_data['id_account'])
            pinjam = int(self.form.cleaned_data['amount'])
            akun = Accounts.objects.get(id_account=id_akun)
            akun.balance = akun.balance + pinjam
            akun.save()
        return redirect('index')

# ===============================================
# === untuk bayar pinjaman ===
# ===============================================
class payloan(LoanAccount, View):
    template_name = 'bank/pay_loan.html'
    form = transaksi()
    mode = None
    context = {}
   
   # === override method get dari parent class view ===
    def get(self, *args, **kwargs):
        print(kwargs)
        self.form = transaksi()
        data_pinjam = Accounttransactions.objects.get(id=kwargs['pinjam_id'])
        data_pinjam.amount = data_pinjam.amount + (data_pinjam.amount*0.1)
        self.context = {
            "page_title":"Pay Loan",
            "tipe":"Pay_loan",
            "id_akun":kwargs['akun_id'],
            "data_pinjam":data_pinjam,
            "transaksi_form":self.form,
        }
        return render(self.request, self.template_name, self.context)

    # === override methode post dari parent class view ===  
    def post(self, *args, **kwargs):
        self.form = transaksi(self.request.POST or None)

        if self.form.is_valid():
            new_transaksi = Accounttransactions(
                id_account = Accounts.objects.get(id_account=self.form.cleaned_data['id_account']),
                type = self.form.cleaned_data['type'],
                amount = self.form.cleaned_data['amount'],
            )
            new_transaksi.save()
            id_akun = str(self.form.cleaned_data['id_account'])
            pinjam = int(self.form.cleaned_data['amount'])
            akun = Accounts.objects.get(id_account=id_akun)
            akun.balance = akun.balance - pinjam
            akun.save()
            pinjam_lunas = Accounttransactions.objects.get(id=self.form.cleaned_data['id_pinjam'])
            pinjam_lunas.amount = 0
            pinjam_lunas.save()
        return redirect('index')


# ===============================================
# === inherite dengan class view ===
# ===============================================
class Customer(View):
    template_name = 'bank/buat_nasabah.html'
    form = createnasabah()
    context = {}
   
    def get(self, *args, **kwargs):
        print("asd")
        self.form = createnasabah()
        self.context = {
            "page_title":"Daftar Nasabah",
            "nasabah_form":self.form,
        }
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        self.form = createnasabah(self.request.POST or None)

        if self.form.is_valid():
            self.form.save()
            
        return redirect('index')

def index(request, customer=0):
    
    form = find()
    
    context = {
        'form': form,
    }

    return render(request,'bank/index.html',context)

def akun(request):
    try:
        nasabah = models.Customers.objects.get(name=request.POST['name'])
        if nasabah:
            accounts = models.Accounts.objects.filter(id_customer=nasabah.id_customer)
        else:
            accounts = models.Accounts.objects.filter(id_customer=0)
        context = {
            'Title':'customer',
            'heading':'customer',
            'accounts':accounts,
            'nasabah':nasabah,
        
        }
        return render(request,'bank/account.html',context)
    except ObjectDoesNotExist:

        return redirect('index')


def tambahakun(request,nasabah_id):
    cek_nasabah = models.Customers.objects.get(id_customer=nasabah_id)
    
    if request.method == 'POST':
        print("asdasdasdasdd")
        akun_form = createakun(request.POST or None)
        if akun_form.is_valid():
            id_nasabah = Customers.objects.get(id_customer=akun_form.cleaned_data['id_customer'])
            add_akun = Accounts(
                id_customer = id_nasabah,
                type = akun_form.cleaned_data['type'],
                balance = akun_form.cleaned_data['balance']
            )
            add_akun.save()
        
        return redirect('index')
    else :
        print("123")
        akun_form = createakun()
    context = {
        "akun_form":akun_form,
        "nasabah":cek_nasabah,
    }

    return render(request,'bank/createakun.html',context)