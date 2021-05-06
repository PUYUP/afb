from django.db import models

# Create your models here.
class Supplier(models.Model):
    namasupplier = models.CharField(max_length=30, db_index=True)
    alamat = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    kota = models.CharField(max_length=20, blank=True, db_index=True)
    kontak = models.CharField(max_length=20, blank=True)
    kontakhp = models.CharField(max_length=15, blank=True)
    teknisi = models.CharField(max_length=20, blank=True)
    teknisihp = models.CharField(max_length=15, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.namasupplier

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Supplier'
        ordering = ['namasupplier']
