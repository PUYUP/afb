import csv
from io import BytesIO

from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

from alatberat.models import Alatberat
from bbm.models import Tangkiinduk, Mobiltangki
from report.utils import reverse_date_format
from report.views import HourmeterReportView, BiayaabPerAlatReportView, BiayaabPerTanggalReportView, BBMabReportView
from report.views import TransaksiTangkiIndukReportView, TransaksiMobilTangkiReportView
from report.views import ProduksiReportView


def get_current_datetime_string():
    now = datetime.now()
    now_string = now.strftime('%Y-%m-%d__%H:%M:%S')
    return now_string


class ExportRendererView(object):
    object_exportables = []

    def get_title(self):
        title = self.title_prefix
        try:
            start_date = reverse_date_format(self.request.GET['start_date'])
            end_date = reverse_date_format(self.request.GET['end_date'])
            title = "{} {} sampai {}".format(title, start_date, end_date)
        except Exception:
            pass
        return title

    def get_filename(self):
        return self.export_filename

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["inner_template_name"] = self.inner_template_name
        return context

    def render_pdf_response(self, context):
        template = get_template('report/pdf_template.html')
        html = template.render(context)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            http_response = HttpResponse(response.getvalue(), content_type='application/pdf')
            return http_response
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    def render_csv_response(self, context):
        response = HttpResponse(content_type='text/csv')
        exportables = ["nomor"] + self.object_exportables
        writer = csv.DictWriter(response, fieldnames=exportables)
        writer.writeheader()
        for counter, obj in enumerate(self.object_list, 1):
            data = {}
            data["nomor"] = counter
            try:
                for key in self.object_exportables:
                    data[key] = getattr(obj, key)
                writer.writerow(data)
            except KeyError as error_message:
                error_message = "No such key '{}'".format(error_message)
                messages.add_message(self.request, messages.ERROR, error_message)
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
        return response

    def render_to_response(self, context, **response_kwargs):
        if not self.object_list:
            return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

        context['title'] = self.get_title()
        if 'export_csv' not in self.request.GET:
            response = self.render_pdf_response(context)
            file_type = 'pdf'
        else:
            response = self.render_csv_response(context)
            file_type = 'csv'
        response['Content-Disposition'] = 'attachment; filename={}.{}'.format(self.get_filename(), file_type)
        return response


class ObjectDetailExportView(ExportRendererView):
    def get_obj_detail(self):
        objectid = int(self.request.GET[self.object_key])
        obj = self.object_model.objects.get(pk=objectid)
        return obj

    def get_filename(self):
        filename = super().get_filename()
        filename = "{}__{}".format(filename, self.get_obj_detail())
        return filename

    def get_title(self):
        title = super().get_title()
        title = "{} ({})".format(title, self.get_obj_detail())
        return title


class HourMeterExportView(ObjectDetailExportView, HourmeterReportView):
    inner_template_name = "report/report_hour_meter_inner.html"
    export_filename = "{}_Hour_Meter".format(get_current_datetime_string())
    title_prefix = "Hour Meter Report"
    object_key = 'alatid'
    object_model = Alatberat
    object_exportables = [
        'tanggal', 'operator_name', 'hmawal',
        'hmakhir', 'jam', 'hmdunia',
        'ot', 'shift', 'keterangan'
    ]


class BiayaabPerAlatExportView(ObjectDetailExportView, BiayaabPerAlatReportView):
    inner_template_name = "report/report_biaya_ab_alat_inner.html"
    export_filename = "{}_Biaya_AB_per_Alat".format(get_current_datetime_string())
    title_prefix = "Biaya Alat Berat"
    object_key = 'alatid'
    object_model = Alatberat
    object_exportables = ['tanggal', 'keterangan', 'biaya']


class BiayaabPerTanggalExportView(ExportRendererView, BiayaabPerTanggalReportView):
    inner_template_name = "report/report_biaya_ab_tanggal_inner.html"
    export_filename = "{}_Biaya_AB_Per_Tanggal".format(get_current_datetime_string())
    title_prefix = "Biaya Alat Berat Per Tanggal"
    object_exportables = ['tanggal', 'alatid', 'keterangan', 'biaya']


class BBMabExportView(ObjectDetailExportView, BBMabReportView):
    inner_template_name = "report/report_bbm_ab_inner.html"
    export_filename = "{}_BBM_Alat_berat".format(get_current_datetime_string())
    title_prefix = "BBM Alat Berat"
    object_key = 'alatid'
    object_model = Alatberat
    object_exportables = ['tanggal', 'hmnow', 'hmbefore', 'ltrmasuk', 'keterangan']


class TransaksiTangkiIndukExportView(ObjectDetailExportView, TransaksiTangkiIndukReportView):
    inner_template_name = "report/report_transaksi_tangki_induk_inner.html"
    export_filename = "{}_Transaksi_Tangki_Induk".format(get_current_datetime_string())
    title_prefix = "Transaksi Tangki Induk"
    object_key = 'tangkiid'
    object_model = Tangkiinduk
    object_exportables = ['tanggal', 'keterangan', 'agentid', 'mobilid', 'masuk', 'keluar', 'amount', 'sisa']


class TransaksiMobilTangkiExportView(ObjectDetailExportView, TransaksiMobilTangkiReportView):
    inner_template_name = "report/report_transaksi_mobil_tangki_inner.html"
    export_filename = "{}_Transaksi_Mobil_Tangki".format(get_current_datetime_string())
    title_prefix = "Transaksi Mobil Tangki"
    object_key = 'mobilid'
    object_model = Mobiltangki
    object_exportables = ['tanggal', 'alatid', 'kendaraanid', 'keluar', 'keterangan']


class ProduksiExportView(ExportRendererView, ProduksiReportView):
    inner_template_name = "report/report_produksi_inner.html"
    export_filename = "{}_Hasil_Produksi".format(get_current_datetime_string())
    title_prefix = "Hasil Produksi"
    object_exportables = ['tanggal', 'hasil', 'keterangan']
