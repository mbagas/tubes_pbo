from django.urls import path, include, re_path

from . import views

urlpatterns = [
     path('',views.index, name='index'),
     path('akun',views.akun),
     path('createakun',views.tambahakun, name='createakun'),
]
