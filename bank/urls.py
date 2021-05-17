from django.urls import path, include, re_path

from . import views

urlpatterns = [
     path('',views.index, name='index'),
     path('akun',views.akun),
     path('createakun/<nasabah_id>/',views.tambahakun, name='createakun'),

     path('transaksi/deposit/<akun_id>',views.Account.as_view(mode="deposit"), name='deposit'),
     path('transaksi/withdraw/<akun_id>',views.Account.as_view(mode="withdraw"), name='withdraw'),
     path('transaksi/BalanceEnquiry/<akun_id>',views.Account.as_view(mode="BalanceEnquiry"), name='BalanceEnquiry'),
]
