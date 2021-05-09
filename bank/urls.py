from django.urls import path, include, re_path

from . import views

urlpatterns = [
     path('',views.index, name='index'),
     path('akun',views.akun),
     path('createakun/<nasabah_id>/',views.tambahakun, name='createakun'),

     path('transaksi/save',views.Account.as_view(mode="deposit"), name='deposit'),
]
