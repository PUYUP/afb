from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .models import Transaksimobiltangki, Transaksitangkiinduk
from .forms import TransaksimobilTangkiAddForm, TransaksitangkiindukAddForm


class TransaksitangkiindukAddView(LoginRequiredMixin, CreateView):
    model = Transaksitangkiinduk
    form_class = TransaksitangkiindukAddForm
    template_name = 'bbm/add_transaksi_tangki_induk.html'
    success_url = '/bbm/add_transaksi_tangki_induk'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Row Added")
        return super().form_valid(form)


class TransaksimobiltangkiAddView(LoginRequiredMixin, CreateView):
    model = Transaksimobiltangki
    form_class = TransaksimobilTangkiAddForm
    template_name = 'bbm/add_transaksi_mobil_tangki.html'
    success_url = '/bbm/add_transaksi_mobil_tangki'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Row Added")
        return super().form_valid(form)
