from django.contrib import admin
from .models import Alatberat, Operatorab, Hourmeter, Biayaab, Bbmab


class AlatberatAdmin(admin.ModelAdmin):
    list_display = ('namaalat', 'hargasewa', 'bbmperjam', 'jenissewa', 'supplier', 'keterangan')
    list_filter = ['supplier']


class OperatorabAdmin(admin.ModelAdmin):
    list_display = ('namaoperator', 'hp', 'basicsalary', 'hadirpagi', 'hadirmalam', 'mingguraya')


class HourmeterAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'operatorid', 'alatid', 'hmawal', 'hmakhir', 'hmdunia', 'ot', 'shift', 'keterangan')
    list_filter = ['alatid', 'tanggal']


class BiayaabAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'alatid', 'biaya', 'keterangan')
    list_filter = ['alatid', 'tanggal']


class BbmabAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'alatid', 'hmnow', 'hmbefore', 'ltrmasuk', 'keterangan')
    list_filter = ['alatid', 'tanggal']


admin.site.register(Alatberat, AlatberatAdmin)
admin.site.register(Operatorab, OperatorabAdmin)
admin.site.register(Hourmeter, HourmeterAdmin)
admin.site.register(Biayaab, BiayaabAdmin)
admin.site.register(Bbmab, BbmabAdmin)
