from django.urls import path, include, re_path
from django.views.generic.base import View

from . import views

urlpatterns = [
     path('',views.index, name='index'),
     path('akun',views.akun),
     path('createakun/<nasabah_id>',views.tambahakun, name='createakun'),
     path('contact',views.contact, name='contact'),
     path('about',views.about, name='about'),

     #class account
     path('transaksi/deposit/<akun_id>',views.Account.as_view(mode="deposit"), name='deposit'),
     path('transaksi/withdraw/<akun_id>',views.Account.as_view(mode="withdraw"), name='withdraw'),
     path('transaksi/BalanceEnquiry/<akun_id>',views.Account.as_view(mode="BalanceEnquiry"), name='BalanceEnquiry'),
     
     #class chechking
     path('transaksi/checkingwithdraw/<akun_id>',views.CheckingAccount.as_view(), name='checkingwithdraw'),

     #class saving
     path('transaksi/savinginterest/<akun_id>', views.SavingAccount.as_view(), name='savinginterest'),

     #class loan
     path('transaksi/loan/<akun_id>',views.LoanAccount.as_view(mode="loan"), name='loan'),

     #class payloan
     path('transaksi/payloan/<akun_id>/<pinjam_id>',views.payloan.as_view(), name='payloan'),

     #class customer
     path('daftar_nasabah', views.Customer.as_view(), name='daftar'),
]
