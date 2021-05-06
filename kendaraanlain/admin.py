from django.contrib import admin
from .models import Kendaraanlain

# Register your models here.

class KendaraanlainAdmin(admin.ModelAdmin):
    list_display = ('nama', 'keterangan')

admin.site.register(Kendaraanlain, KendaraanlainAdmin)
