from django.contrib import admin
from .models import Hasilore

class HasiloreAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'hasil', 'keterangan')

admin.site.register(Hasilore, HasiloreAdmin)
