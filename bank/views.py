from django.shortcuts import render, redirect

# Create your views here.

from . import models
from .form import find
from .form import createakun

def index(request, customer=0):
    
    form = find()
    
    context = {
        'form': form,
    }

    return render(request,'bank/index.html',context)

def akun(request):
    form = find()
    # nasabah = models.Customers.objects.values_list('id_customer', flat=True).filter(name=request.POST['name'])
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

    if request.method == 'POST':
        if akun_form.is_valid():
            akun_form.save()
        
        return redirect('index')
    
    context = {
        "akun_form":akun_form,
        "nasabah":cek_nasabah,
    }

    return render(request,'bank/createakun.html',context)