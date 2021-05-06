from django.db import models
import datetime


# Create your models here.
class Tangkiinduk(models.Model):
    nama = models.CharField(max_length=20)
    keterangan = models.CharField(max_length=50, default=None, blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = 'Daftar Tangki Induk'
        verbose_name_plural = 'Daftar Tangki Induk'
        ordering = ['nama']


class Mobiltangki(models.Model):
    nama = models.CharField(max_length=20)
    keterangan = models.CharField(max_length=50, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = 'Daftar Mobil Tangki'
        verbose_name_plural = 'Daftar Mobil Tangki'
        ordering = ['nama']


class Agent(models.Model):
    nama = models.CharField(max_length=20)
    alamat = models.CharField(max_length=100)
    telp = models.CharField(max_length=20)

    def __str__(self):
        return self.nama


# Historical based on Tangki Induk
class Transaksitangkiinduk(models.Model):
    tanggal = models.DateField()
    tangkiid = models.ForeignKey('Tangkiinduk', on_delete=models.CASCADE)
    agentid = models.ForeignKey('Agent', on_delete=models.CASCADE)
    masuk = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mobilid = models.ForeignKey('Mobiltangki', on_delete=models.CASCADE, null=True, blank=True)
    keluar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    keterangan = models.CharField(max_length=50, default=None, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaksi Tangki Induk'
        verbose_name_plural = 'Transaksi Tangki Induk'
        ordering = ['tanggal']


# Historical based on Mobil Tangki
class Transaksimobiltangki(models.Model):
    tanggal = models.DateField()
    mobilid = models.ForeignKey('Mobiltangki', on_delete=models.CASCADE)
    keluar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    alatid = models.ForeignKey('alatberat.Alatberat', on_delete=models.CASCADE, null=True, blank=True, help_text="Alat berat yg menggunakan BBM")
    kendaraanid = models.ForeignKey('kendaraanlain.Kendaraanlain', on_delete=models.CASCADE, null=True, blank=True, help_text="Kendaraan / alat lain pengguna BBM")
    keterangan = models.CharField(max_length=50, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaksi Mobil Tangki'
        verbose_name_plural = 'Transaksi Mobil Tangki'
        ordering = ['tanggal']
