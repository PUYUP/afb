from afb.forms import AFBForm
from alatberat.models import Alatberat
from bbm.models import Mobiltangki, Tangkiinduk, Transaksimobiltangki, Transaksitangkiinduk, Agent
from kendaraanlain.models import Kendaraanlain


class TransaksitangkiindukAddForm(AFBForm):
    class Meta:
        model = Transaksitangkiinduk
        fields = ('tanggal', 'agentid', 'tangkiid', 'masuk', 'mobilid', 'keluar', 'keterangan', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tangkiid'].queryset = Tangkiinduk.objects.all()
        self.fields['mobilid'].queryset = Mobiltangki.objects.all()
        self.fields['agentid'].queryset = Agent.objects.all()


class TransaksimobilTangkiAddForm(AFBForm):
    class Meta:
        model = Transaksimobiltangki
        fields = ('tanggal', 'mobilid', 'keluar', 'alatid', 'kendaraanid', 'keterangan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobilid'].queryset = Mobiltangki.objects.all()
        self.fields['alatid'].queryset = Alatberat.objects.all()
        self.fields['kendaraanid'].queryset = Kendaraanlain.objects.all()
