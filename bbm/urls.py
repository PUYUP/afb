from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_transaksi_tangki_induk/$', views.TransaksitangkiindukAddView.as_view(), name='add_transaksi_tangki_induk'),
    url(r'^add_transaksi_mobil_tangki/$', views.TransaksimobiltangkiAddView.as_view(), name='add_transaksi_mobil_tangki'),
]
