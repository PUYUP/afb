from django.db import models
import datetime


# Create your models here.
# Historical
class Hasilore(models.Model):
    tanggal = models.DateField(db_index=True, default=datetime.datetime.now)
    hasil = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=50, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return format(self.tanggal, "%d-%m-%Y")

    class Meta:
        verbose_name = 'Hasil Ore'
        verbose_name_plural = 'Hasil Ore'
        ordering = ['-tanggal']
