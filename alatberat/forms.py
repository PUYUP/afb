from afb.forms import AFBForm
from alatberat.models import Alatberat, Biayaab, Hourmeter, Operatorab


class BiayaabAddForm(AFBForm):
    class Meta:
        model = Biayaab
        fields = ('alatid', 'tanggal', 'biaya', 'keterangan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alatid'].queryset = Alatberat.objects.all()


class HourMeterAddForm(AFBForm):
    class Meta:
        model = Hourmeter
        fields = ('alatid', 'operatorid', 'tanggal', 'hmawal', 'hmakhir', 'hmdunia', 'ot', 'shift', 'keterangan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alatid'].queryset = Alatberat.objects.all()
        self.fields['operatorid'].queryset = Operatorab.objects.all()
