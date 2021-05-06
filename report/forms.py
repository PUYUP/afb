from django import forms

from alatberat.models import Hourmeter, Alatberat, Operatorab, Biayaab, Bbmab
from bbm.models import Mobiltangki, Tangkiinduk, Transaksitangkiinduk, Transaksimobiltangki
from .utils import reverse_date_format

"""
ALAT BERAT FORM
"""


# Mixin for date range form
class DateRangeFormMixin(forms.Form):
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs = {'class': 'form-control mr-3', "placeholder": "Start Date"}
        self.fields['end_date'].widget.attrs = {'class': 'form-control mr-3', "placeholder": "End Date"}

    def clean_start_date(self):
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        if start_date > end_date:
            raise forms.ValidationError('Mohon periksa kembali tanggal pencarian anda')
        return reverse_date_format(start_date)

    def clean_end_date(self):
        end_date = self.data['end_date']
        return reverse_date_format(end_date)


class HourmeterReportForm(DateRangeFormMixin, forms.ModelForm):
    class Meta:
        model = Hourmeter
        fields = ('alatid', 'operatorid')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alatid'].widget.attrs = {'class': 'form-control mr-3'}
        self.fields['operatorid'].widget.attrs = {'class': 'form-control mr-3'}
        self.fields['alatid'].queryset = Alatberat.objects.all()
        self.fields['operatorid'].queryset = Operatorab.objects.all()


class BiayaPerAlatReportForm(DateRangeFormMixin, forms.ModelForm):
    class Meta:
        model = Biayaab
        fields = ('alatid', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alatid'].widget.attrs = {'class': 'form-control mr-3'}
        self.fields['alatid'].queryset = Alatberat.objects.all()


class BiayaPerTanggalReportForm(DateRangeFormMixin):
    pass


# Inherit Biaya per alat form due to the similarity
class BBMReportForm(BiayaPerAlatReportForm):
    class Meta:
        model = Bbmab
        fields = ('alatid', 'start_date', 'end_date')


class TransaksiTangkiIndukForm(DateRangeFormMixin, forms.ModelForm):
    class Meta:
        model = Transaksitangkiinduk
        fields = ('tangkiid', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tangkiid'].widget.attrs = {'class': 'form-control mr-3'}
        self.fields['tangkiid'].queryset = Tangkiinduk.objects.all()


class TransaksiMobilTangkiForm(DateRangeFormMixin, forms.ModelForm):
    class Meta:
        model = Transaksimobiltangki
        fields = ('mobilid', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobilid'].widget.attrs = {'class': 'form-control mr-3'}
        self.fields['mobilid'].queryset = Mobiltangki.objects.all()


class ProduksiReportForm(DateRangeFormMixin):
    pass
