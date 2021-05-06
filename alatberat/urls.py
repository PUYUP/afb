from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_biaya_ab/$', views.BiayaabAddView.as_view(), name='add_biaya_ab'),
    url(r'^add_hour_meter/$', views.HourmeterAddView.as_view(), name='add_hour_meter')
]
