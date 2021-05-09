from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View

# Create your views here.

from . import models
from .form import find
from .form import createakun
from .form import transaksi

class Account(View):
    template_name = 'bank/transaksi.html'
    form = transaksi()
    mode = None
    context = {}

    def get(self, *args, **kwargs):

        if self.mode == 'deposit':
            print("asd")
            # akun_id = models.Accounts.objects.get(id_account=kwargs['akun_id'])
            
            self.form = transaksi()
            self.context = {
                "page_title":"deposit",
                "tipe":"deposit",
                "transaksi_form":self.form,
                # "nasabah":akun_id,
            }
        print("qwe")
        return render(self.request, self.template_name, self.context)
        
    def post(self, *args, **kwargs):

        self.form = transaksi(self.request.POST or None)
        
        if self.form.is_valid():
            print(self.form)
            self.form.save()
        
        return redirect('index')


def index(request, customer=0):
    
    form = find()
    
    context = {
        'form': form,
    }

    return render(request,'bank/index.html',context)

def akun(request):
    form = find()
    nasabah = models.Customers.objects.get(name=request.POST['name'])
    print(nasabah.id_customer)
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
    print(akun_form)
    if request.method == 'POST':
        if akun_form.is_valid():
            akun_form.save()
        
        return redirect('index')
    
    context = {
        "akun_form":akun_form,
        "nasabah":cek_nasabah,
    }

    return render(request,'bank/createakun.html',context)