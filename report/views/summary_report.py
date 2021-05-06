from datetime import date, datetime, timedelta
from calendar import weekday, monthrange, SUNDAY, monthcalendar

from django.shortcuts import render
from django.db.models import Q, F, Sum, Max, Count, FloatField, IntegerField, ExpressionWrapper
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.db.models.functions import ExtractWeekDay

from alatberat.models import Bbmab, Biayaab, Hourmeter, Operatorab, Alatberat
from bbm.models import Transaksitangkiinduk, Transaksimobiltangki
from produksi.models import Hasilore

from report.forms import (
    HourmeterReportForm, BiayaPerAlatReportForm, BiayaPerTanggalReportForm,
    BBMReportForm)


class ReportOperatorView(View):
    """ Summary operator report """
    template_name = 'report/report_summary_operator.html'
    form = HourmeterReportForm
    valid_keys = ['alatid', 'operatorid', 'start_date', 'end_date']
    context = {}
    alatid = None
    operatorid = None
    start_date = None
    end_date = None

    # Prepare fields
    fields_value = Hourmeter._meta.get_fields()
    fields_initial = {}

    # Inject values to form
    def get_fields_value(self):
        for field in self.fields_value:
            self.fields_initial[field.name] = getattr(
                self, field.name, None)
        return self.fields_initial

    # GET request
    def get(self, request, *args, **kwargs):
        # Get variable from request
        get_var = self.request.GET
        reports_obj = None
        reports_obj_row = None
        reports_obj_summary = None
        reports_obj_summary_total = None

        # Ensure all parameters are not empty
        if get_var and all(key in get_var for key in self.valid_keys):
            self.alatid = get_var['alatid']
            self.operatorid = get_var['operatorid']
            self.start_date = get_var['start_date']
            self.end_date = get_var['end_date']

            self.start_date = datetime.strptime(
                self.start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
            self.end_date = datetime.strptime(
                self.end_date, '%d-%m-%Y').strftime('%Y-%m-%d')

            reports_obj = Hourmeter.objects \
                .annotate(
                    total_hmawal=Sum('hmawal'),
                    total_hmakhir=Sum('hmakhir'),
                    total_jam=Sum('hmakhir') - Sum('hmawal')
                ) \
                .filter(
                    alatid__pk=self.alatid,
                    operatorid__pk=self.operatorid,
                    tanggal__range=[self.start_date, self.end_date]
                )

            if reports_obj is not None:
                reports_obj_row = reports_obj \
                    .aggregate(
                        total_hmawal_row=Sum('hmawal'),
                        total_hmakhir_row=Sum('hmakhir'),
                        total_hmdunia_row=Sum('hmdunia'),
                        total_jam_row=Sum('total_jam'),
                        total_ot_row=Sum('ot')
                    )

                # Count shift by operator and group by shift
                reports_obj_summary = reports_obj \
                    .values('shift') \
                    .annotate(
                        total_hadir=Count('operatorid'),
                        total_jam=Sum('hmakhir') - Sum('hmawal'),
                        total_hmdunia=Sum('hmdunia'),
                        total_ot=Sum('ot')
                    ).order_by('total_hadir')

                reports_obj_summary_total = reports_obj \
                    .values('shift') \
                    .order_by('total_hadir') \
                    .aggregate(
                        total_hadir=Count('operatorid'),
                        total_jam=Sum('hmakhir') - Sum('hmawal'),
                        total_hmdunia=Sum('hmdunia'),
                        total_ot=Sum('ot')
                    )

                # Count sunday from date range
                d_start = datetime.strptime(self.start_date, "%Y-%m-%d")
                d_end = datetime.strptime(self.end_date, "%Y-%m-%d")
                delta_date = d_end - d_start
                delta_total = delta_date.days

                total_minggu = []
                for i in range(1, delta_total):
                    yesterday = datetime.now() - timedelta(days=i)
                    if yesterday.weekday() == 6:
                        total_minggu.append(yesterday.strftime('%Y-%m-%d'))

        self.context['form'] = self.form(initial=self.get_fields_value())
        self.context['reports_obj'] = reports_obj
        self.context['reports_obj_row'] = reports_obj_row
        self.context['reports_obj_summary'] = reports_obj_summary
        self.context['reports_obj_summary_total'] = reports_obj_summary_total
        self.context['start_date'] = self.start_date
        self.context['end_date'] = self.end_date
        self.context['total_minggu'] = len(
            total_minggu) if reports_obj is not None else None
        return render(request, self.template_name, self.context)

    # POST request
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            self.alatid = form.cleaned_data['alatid'].id
            self.operatorid = form.cleaned_data['operatorid'].id
            self.start_date = form.cleaned_data['start_date']
            self.end_date = form.cleaned_data['end_date']

            self.start_date = datetime.strptime(
                self.start_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            self.end_date = datetime.strptime(
                self.end_date, '%m-%d-%Y').strftime('%Y-%m-%d')

            querystring = "?alatid={}&operatorid={}&start_date={}" \
                "&end_date={}" \
                .format(self.alatid, self.operatorid, self.start_date,
                        self.end_date)

            return HttpResponseRedirect(
                reverse('report:summary_report_operator') + querystring)
        return render(request, self.template_name, self.context)


class ReportGajiView(View):
    """ Summary report sallary by operator per month """
    template_name = 'report/report_summary_gaji.html'
    context = {}
    start_date = None
    end_date = None

    # GET request
    def get(self, request, *args, **kwargs):
        month = 7
        year = 2019

        # Extract sunday date from month
        month_sunday = []
        month_calendar = monthcalendar(year, month)
        for i in month_calendar:
            if i[6] > 0:
                d = datetime(year, month, i[6])
                month_sunday.append(d.strftime('%Y-%m-%d'))

        # Filter by month
        reports_obj = Hourmeter.objects \
            .values(
                'alatid', 'alatid__namaalat', 'operatorid__namaoperator',
                'operatorid__basicsalary', 'tanggal'
            ) \
            .annotate(
                total_gaji=Count('operatorid__basicsalary')
            ) \
            .filter(
                tanggal__month=month,
                tanggal__year=year
            ).order_by('operatorid__namaoperator')

        # Grop by shift
        reports_obj_shift = reports_obj \
            .values(
                'shift', 'operatorid', 'operatorid__namaoperator',
                'operatorid__hadirpagi', 'operatorid__hadirmalam',
                'hmakhir', 'hmawal', 'alatid__hargahm', 'alatid__hargaot'
            ) \
            .annotate(
                total_hadir=Count('operatorid'),
                total_uang_hadirpagi=Sum('operatorid__hadirpagi'),
                total_uang_hadirmalam=Sum('operatorid__hadirmalam'),
                total_jam=Sum(F('hmakhir')) - Sum(F('hmawal')),
                total_uang_jam=F('alatid__hargahm') * F('total_jam'),
                total_ot=Sum('ot'),
                total_uang_ot=F('total_ot') * F('alatid__hargaot')
            ).order_by('shift')

        # Group by operator
        reports_obj_operator = reports_obj \
            .values(
                'operatorid', 'operatorid__namaoperator', 'alatid__namaalat',
                'operatorid__basicsalary', 'operatorid__mingguraya',
                'operatorid__bpjs'
            ) \
            .annotate(
                total_hadir=Count('operatorid')
            ).order_by('operatorid')
        
        # Group by holidays
        reports_obj_holiday = reports_obj \
            .values(
                'operatorid', 'operatorid__namaoperator'
            ) \
            .annotate(
                kerja_hari_libur=Count('operatorid'),
                total_uang_libur=ExpressionWrapper(
                    F('kerja_hari_libur') * F('operatorid__mingguraya'),
                    output_field=FloatField())
            ) \
            .filter(
                tanggal__in=month_sunday
            ).order_by('-kerja_hari_libur')

        # Group shift by operator
        results_shift = {}
        for item in reports_obj_shift:
            results_shift.setdefault(item['operatorid'], []).append(item)
        
        # Group holidays by operator
        results_holiday = {}
        for item in reports_obj_holiday:
            results_holiday.setdefault(item['operatorid'], []).append(item)

        # Append shift to operator
        reports_obj_result = []
        for item in reports_obj_operator:
            shift = results_shift[item['operatorid']]
            holiday = results_holiday.get(item['operatorid'])
            data = {
                'data_shift': shift,
                'data_item': item,
                'data_holiday': holiday[0] if holiday is not None else None
            }
            reports_obj_result.append(data)

        self.context['month_sunday'] = month_sunday
        self.context['reports_obj'] = reports_obj
        self.context['reports_obj_operator'] = reports_obj_operator
        self.context['reports_obj_result'] = reports_obj_result
        self.context['reports_obj_holiday'] = reports_obj_holiday
        self.context['results_holiday'] = results_holiday
        return render(request, self.template_name, self.context)

    # POST request
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
