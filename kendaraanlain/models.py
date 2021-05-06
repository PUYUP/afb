from django.db import models


# Create your models here.
class Kendaraanlain(models.Model):
    nama = models.CharField(max_length=30)
    keterangan = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = 'Kendaraan / Peralatan lainnya'
        verbose_name_plural = 'Kendaraan / Peralatan lainnya'
        ordering = ['nama']
