from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from alatberat.models import Bbmab, Biayaab, Hourmeter
from bbm.models import Transaksitangkiinduk, Transaksimobiltangki
from produksi.models import Hasilore

from report.forms import (
    HourmeterReportForm, BiayaPerAlatReportForm, BiayaPerTanggalReportForm,
    BBMReportForm)
from report.forms import TransaksiTangkiIndukForm, TransaksiMobilTangkiForm
from report.forms import ProduksiReportForm

from utils.generals import proper_paginate


# REPORT INDEX
class ReportIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'report/index.html'


# REPORT ALAT BERAT
class HourmeterReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_hour_meter.html'
    model = Hourmeter
    valid_keys = ['alatid', 'operatorid', 'start_date', 'end_date']
    prefilled_keys = ['alatid', 'operatorid']
    form = HourmeterReportForm

    paginate_by = 0
    alat_id = None
    operator_id = None
    start_date = None
    end_date = None

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        # Ensure all parameters are not empty
        if get_var and all(key in get_var for key in self.valid_keys):
            # Activate pagination if request has parameters
            self.paginate_by = 10

            self.alat_id = get_var['alatid']
            self.operator_id = get_var['operatorid']
            self.start_date = get_var['start_date']
            self.end_date = get_var['end_date']

            queryset = self.model.objects.filter(
                alatid_id=int(self.alat_id), operatorid_id=int(self.operator_id),
                tanggal__range=[self.start_date, self.end_date]
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total_jam = 0
        total_hm_dunia = 0
        total_overtime = 0
        form_data = {}

        # Paginate variable
        reports_obj = None
        the_pagination = None

        # If paginated allowed
        if self.paginate_by > 0:
            page = int(self.request.GET.get('page', 1))
            paginator = Paginator(self.get_queryset(), self.paginate_by)
            try:
                reports_obj = paginator.page(page)
            except PageNotAnInteger:
                reports_obj = paginator.page(1)
            except EmptyPage:
                reports_obj = paginator.page(paginator.num_pages)

            the_pagination = proper_paginate(
                paginator, page, self.paginate_by)

        for key in self.prefilled_keys:
            try:
                form_data[key] = self.request.GET[key]
            except KeyError:
                pass
        form = self.form(data=form_data)

        if context['object_list']:
            for obj in context['object_list']:
                total_jam += obj.jam
                total_hm_dunia += obj.hmdunia
                total_overtime += obj.ot
        context['total_jam'] = total_jam
        context['total_hm_dunia'] = total_hm_dunia
        context['total_overtime'] = total_overtime
        context['form'] = form

        # Paginate objects
        context['alat_id'] = self.alat_id
        context['operator_id'] = self.operator_id
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['reports_obj'] = reports_obj
        context['proper_paginate'] = the_pagination
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    alatid = form.cleaned_data['alatid'].id
                    operatorid = form.cleaned_data['operatorid'].id
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?alatid={}&operatorid={}&start_date={}&end_date={}".format(
                        alatid, operatorid, start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:hour_meter') + querystring)


class BiayaabPerAlatReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_biaya_ab_alat.html'
    model = Biayaab
    valid_keys = ['alatid', 'start_date', 'end_date']
    prefilled_keys = ['alatid']
    form = BiayaPerAlatReportForm

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        if get_var:
            # Ensure all parameters are not empty
            if all(key in get_var for key in self.valid_keys):
                alat_id = get_var['alatid']
                start_date = get_var['start_date']
                end_date = get_var['end_date']

                queryset = self.model.objects.filter(
                    alatid_id=int(alat_id),
                    tanggal__range=[start_date, end_date]
                )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total = 0
        form_data = {}

        for key in self.prefilled_keys:
            try:
                form_data[key] = self.request.GET[key]
            except KeyError:
                pass
        form = self.form(data=form_data)

        if context['object_list']:
            for obj in context['object_list']:
                total += obj.biaya
        context['total'] = total
        context['form'] = form
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    alatid = form.cleaned_data['alatid'].id
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?alatid={}&start_date={}&end_date={}".format(
                        alatid, start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:biaya_per_alat') +
                                    querystring)


class BiayaabPerTanggalReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_biaya_ab_tanggal.html'
    model = Biayaab
    valid_keys = ['start_date', 'end_date']
    form = BiayaPerTanggalReportForm

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        if get_var:
            # Ensure all parameters are not empty
            if all(key in get_var for key in self.valid_keys):
                start_date = get_var['start_date']
                end_date = get_var['end_date']

                queryset = self.model.objects.filter(
                    tanggal__range=[start_date, end_date]
                )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total = 0

        if context['object_list']:
            for obj in context['object_list']:
                total += obj.biaya
        context['total'] = total
        context['form'] = self.form
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?start_date={}&end_date={}".format(
                        start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:biaya_per_tanggal') +
                                    querystring)


class BBMabReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_bbm_ab.html'
    model = Bbmab
    valid_keys = ['alatid', 'start_date', 'end_date']
    prefilled_keys = ['alatid']
    form = BBMReportForm

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        if get_var:
            # Ensure all parameters are not empty
            if all(key in get_var for key in self.valid_keys):
                alat_id = get_var['alatid']
                start_date = get_var['start_date']
                end_date = get_var['end_date']

                queryset = self.model.objects.filter(
                    alatid_id=int(alat_id),
                    tanggal__range=[start_date, end_date]
                )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total_bbm = 0
        form_data = {}

        for key in self.prefilled_keys:
            try:
                form_data[key] = self.request.GET[key]
            except KeyError:
                pass
        form = self.form(data=form_data)

        if context['object_list']:
            for obj in context['object_list']:
                total_bbm += obj.ltrmasuk
        context['total_bbm'] = total_bbm
        context['form'] = form
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    alatid = form.cleaned_data['alatid'].id
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?alatid={}&start_date={}&end_date={}".format(
                        alatid, start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:bbm_ab') + querystring)


# REPORT BBM
class TransaksiTangkiIndukReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_transaksi_tangki_induk.html'
    model = Transaksitangkiinduk
    valid_keys = ['tangkiid', 'start_date', 'end_date']
    prefilled_keys = ['tangkiid']
    form = TransaksiTangkiIndukForm

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        if get_var:
            # Ensure all parameters are not empty
            if all(key in get_var for key in self.valid_keys):
                tangkiid = get_var['tangkiid']
                start_date = get_var['start_date']
                end_date = get_var['end_date']

                queryset = self.model.objects.filter(
                    tangkiid_id=int(tangkiid),
                    tanggal__range=[start_date, end_date]
                )

                previous_queryset = self.model.objects.filter(
                    tangkiid=int(tangkiid), tanggal__lt=start_date
                )

                if previous_queryset:
                    previous_aggregate = previous_queryset.aggregate(
                        masuk=Sum('masuk'), keluar=Sum('keluar'))
                    self.saldo_awal = previous_aggregate['masuk'] - \
                        previous_aggregate['keluar']
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        saldo_awal = 0
        sisa = 0
        total_masuk = 0
        total_keluar = 0
        total_amount = 0
        form_data = {}

        for key in self.prefilled_keys:
            try:
                form_data[key] = self.request.GET[key]
            except KeyError:
                pass
        form = self.form(data=form_data)

        if hasattr(self, 'saldo_awal'):
            saldo_awal = self.saldo_awal
            sisa = saldo_awal

        if context['object_list']:
            for obj in context['object_list']:
                total_masuk += obj.masuk
                total_keluar += obj.keluar
                total_amount += obj.amount
                # variable set on the fly, not based on db record
                sisa = sisa + obj.masuk - obj.keluar
                obj.sisa = sisa

        context['saldo_awal'] = saldo_awal
        context['total_masuk'] = total_masuk
        context['total_keluar'] = total_keluar
        context['total_amount'] = total_amount
        context['form'] = form
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    tangkiid = form.cleaned_data['tangkiid'].id
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?tangkiid={}&start_date={}&end_date={}".format(
                        tangkiid, start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:transaksi_tangki_induk') +
                                    querystring)


class TransaksiMobilTangkiReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_transaksi_mobil_tangki.html'
    model = Transaksimobiltangki
    valid_keys = ['mobilid', 'start_date', 'end_date']
    prefilled_keys = ['mobilid']
    form = TransaksiMobilTangkiForm

    paginate_by = 0
    mobilid = None
    start_date = None
    end_date = None

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        # Ensure all parameters are not empty
        if get_var and all(key in get_var for key in self.valid_keys):
            # Activate pagination if request has parameters
            self.paginate_by = 10
        
            self.mobilid = get_var['mobilid']
            self.start_date = get_var['start_date']
            self.end_date = get_var['end_date']

            queryset = self.model.objects.filter(
                mobilid_id=int(self.mobilid),
                tanggal__range=[self.start_date, self.end_date]
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total_keluar = 0
        form_data = {}

        # Paginate variable
        reports_obj = None
        the_pagination = None

        # If paginated allowed
        if self.paginate_by > 0:
            page = int(self.request.GET.get('page', 1))
            paginator = Paginator(self.get_queryset(), self.paginate_by)
            try:
                reports_obj = paginator.page(page)
            except PageNotAnInteger:
                reports_obj = paginator.page(1)
            except EmptyPage:
                reports_obj = paginator.page(paginator.num_pages)

            the_pagination = proper_paginate(
                paginator, page, self.paginate_by)

        for key in self.prefilled_keys:
            try:
                form_data[key] = self.request.GET[key]
            except KeyError:
                pass
        form = self.form(data=form_data)

        if context['object_list']:
            for obj in context['object_list']:
                total_keluar += obj.keluar
        context['total_keluar'] = total_keluar
        context['form'] = form

        # Paginate objects
        context['mobilid'] = self.mobilid
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['reports_obj'] = reports_obj
        context['proper_paginate'] = the_pagination
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    mobilid = form.cleaned_data['mobilid'].id
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?mobilid={}&start_date={}&end_date={}".format(
                        mobilid, start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:transaksi_mobil_tangki') +
                                    querystring)


# REPORT PRODUKSI
class ProduksiReportView(LoginRequiredMixin, ListView):
    template_name = 'report/report_produksi.html'
    model = Hasilore
    valid_keys = ['start_date', 'end_date']
    form = ProduksiReportForm

    def get_queryset(self):
        queryset = None
        get_var = self.request.GET

        if get_var:
            # Ensure all parameters are not empty
            if all(key in get_var for key in self.valid_keys):
                start_date = get_var['start_date']
                end_date = get_var['end_date']

                queryset = self.model.objects.filter(
                    tanggal__range=[start_date, end_date]
                )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        total_hasil = 0

        if context['object_list']:
            for obj in context['object_list']:
                total_hasil += obj.hasil
        context['total_hasil'] = total_hasil
        context['form'] = self.form
        return context

    def post(self, request):
        querystring = ""
        post_var = request.POST

        if post_var:
            if all(key in post_var for key in self.valid_keys):
                form = self.form(data=post_var)
                if form.is_valid():
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']

                    querystring = "?start_date={}&end_date={}".format(
                        start_date, end_date
                    )
                else:
                    messages.add_message(request, messages.ERROR, form.errors)

        return HttpResponseRedirect(reverse('report:hasil_produksi') +
                                    querystring)
