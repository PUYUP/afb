from django.contrib import admin
from .models import Supplier

# Register your models here.

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('namasupplier', 'alamat', 'kota', 'kontak', 'kontakhp')
    list_filter = ['kota']
    search_fields = ['namasupplier', 'alamat']

admin.site.register(Supplier, SupplierAdmin)
