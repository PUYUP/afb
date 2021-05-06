from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .models import Biayaab, Hourmeter
from .forms import BiayaabAddForm, HourMeterAddForm


class BiayaabAddView(LoginRequiredMixin, CreateView):
    model = Biayaab
    form_class = BiayaabAddForm
    template_name = 'alatberat/add_biaya_ab.html'
    success_url = '/alatberat/add_biaya_ab'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Row Added")
        return super().form_valid(form)


class HourmeterAddView(LoginRequiredMixin, CreateView):
    model = Hourmeter
    form_class = HourMeterAddForm
    template_name = 'alatberat/add_hour_meter.html'
    success_url = '/alatberat/add_hour_meter'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Row Added")
        return super().form_valid(form)
