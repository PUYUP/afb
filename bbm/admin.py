from django.contrib import admin
from .models import Tangkiinduk, Mobiltangki, Transaksitangkiinduk, Transaksimobiltangki, Agent


class AgentAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'telp')
    list_filter = ['nama']


class TangkiindukAdmin(admin.ModelAdmin):
    list_display = ('nama', 'keterangan')


class MobiltangkiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'keterangan')


class TransaksitangkiindukAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'tangkiid', 'agentid', 'masuk', 'mobilid', 'keluar', 'keterangan', 'amount')


class TransaksimobiltangkiAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'mobilid', 'alatid', 'keluar', 'keterangan')


admin.site.register(Tangkiinduk, TangkiindukAdmin)
admin.site.register(Mobiltangki, MobiltangkiAdmin)
admin.site.register(Transaksitangkiinduk, TransaksitangkiindukAdmin)
admin.site.register(Transaksimobiltangki, TransaksimobiltangkiAdmin)
admin.site.register(Agent, AgentAdmin)
