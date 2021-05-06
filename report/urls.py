from django.conf.urls import url

from . import views
from .views import export as export_views
from .views import summary_report

urlpatterns = [
    url(r'^$', views.ReportIndexView.as_view(), name='index'),
    url(r'^hour_meter$', views.HourmeterReportView.as_view(), name='hour_meter'),
    url(r'^biaya_per_alat$', views.BiayaabPerAlatReportView.as_view(), name='biaya_per_alat'),
    url(r'^biaya_per_tanggal$', views. BiayaabPerTanggalReportView.as_view(), name='biaya_per_tanggal'),
    url(r'^bbm_alat_berat$', views.BBMabReportView.as_view(), name='bbm_ab'),
    url(r'^transaksi_tangki_induk$', views.TransaksiTangkiIndukReportView.as_view(), name='transaksi_tangki_induk'),
    url(r'^transaksi_mobil_tangki$', views.TransaksiMobilTangkiReportView.as_view(), name='transaksi_mobil_tangki'),
    url(r'^hasil_produksi$', views.ProduksiReportView.as_view(), name='hasil_produksi'),
    url(r'^export_hour_meter$', export_views.HourMeterExportView.as_view(), name='export_hour_meter'),
    url(r'^export_biaya_per_alat$', export_views.BiayaabPerAlatExportView.as_view(), name='export_biaya_per_alat'),
    url(r'^export_biaya_per_tanggal$', export_views.BiayaabPerTanggalExportView.as_view(), name='export_biaya_per_tanggal'),
    url(r'^export_bbm_ab$', export_views.BBMabExportView.as_view(), name='export_bbm_ab'),
    url(r'^export_transaksi_tangki_induk', export_views.TransaksiTangkiIndukExportView.as_view(), name='export_transaksi_tangki_induk'),
    url(r'^export_transaksi_mobil_tangki', export_views.TransaksiMobilTangkiExportView.as_view(), name='export_transaksi_mobil_tangki'),
    url(r'^export_produksi', export_views.ProduksiExportView.as_view(), name='export_produksi'),

    # Summary reports view
    url(r'^summary_report_operator', summary_report.ReportOperatorView.as_view(),
        name='summary_report_operator'),
    url(r'^summary_report_gaji', summary_report.ReportGajiView.as_view(),
        name='summary_report_gaji'),
]
