from django.shortcuts import render

# Create your views here.

from . import models

def index(request):
    transaksi = models.Accounttransactions.objects.all()
    context = {
        'Title':'customer',
        'heading':'customer',
        'transaksi':transaksi
    }

    return render(request,'bank/index.html',context)