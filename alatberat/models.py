from django.db import models
import datetime

# Create your models here.
ITEM_SHIFT = (
    ('PAGI', 'PAGI'),
    ('SIANG', 'SIANG'),
    ('MALAM', 'MALAM'),
)

ITEM_JENISSEWA = (
    ('JAM', 'JAM'),
    ('BULAN', 'BULAN'),
)


class Alatberat(models.Model):
    namaalat = models.CharField(max_length=30, verbose_name="Nama Alat")
    hargasewa = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Harga Sewa")
    jenissewa = models.CharField(choices=ITEM_JENISSEWA, max_length=10)
    supplier = models.ForeignKey('supplier.supplier', on_delete=models.PROTECT)
    hargahm = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Harga Hour Meter")
    hargaot = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Harga Overtime")
    bbmperjam = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Pemakaian BBM Per Jam")
    jadwalhmservice = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Jadwal HM Service alat",
                      verbose_name="Jadwal HM Service berkala kendaraan")
    keterangan = models.TextField(default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.namaalat

    class Meta:
        verbose_name = 'Alat Berat'
        verbose_name_plural = 'Alat Berat'
        ordering = ['namaalat']


class Operatorab(models.Model):
    namaoperator = models.CharField(max_length=30, verbose_name="Nama Operator")
    alamat = models.CharField(max_length=30, blank=True)
    hp = models.CharField(max_length=15, blank=True)
    foto = models.ImageField(upload_to='foto/', blank=True)
    catatan = models.TextField(default=None, blank=True)
    basicsalary = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Basic Salary")
    hadirpagi = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    hadirmalam = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mingguraya = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    bpjs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.namaoperator

    class Meta:
        verbose_name = 'Operator Alat Berat'
        verbose_name_plural = 'Operator Alat Berat'
        ordering = ['namaoperator']


# Historical based on alat berat and date range
class Hourmeter(models.Model):
    alatid = models.ForeignKey('Alatberat', on_delete=models.CASCADE)
    operatorid = models.ForeignKey('Operatorab', on_delete=models.CASCADE, db_index=True)
    tanggal = models.DateField(db_index=True, default=datetime.datetime.now)
    hmawal = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="HM Awal")
    hmakhir = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    hmdunia = models.DecimalField(max_digits=10, decimal_places=0, default=9, verbose_name="HM Dunia")
    ot = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Overtime")
    shift = models.CharField(choices=ITEM_SHIFT, max_length=5)
    keterangan = models.CharField(max_length=20, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return format(self.tanggal, "%d-%m-%Y")

    @property
    def operator_name(self):
        return self.operatorid.namaoperator

    @property
    def jam(self):
        return self.hmakhir - self.hmawal

    class Meta:
        verbose_name = 'Hour Meter'
        verbose_name_plural = 'Hour Meter'
        ordering = ['-tanggal']


# Historical based on alat berat
class Biayaab(models.Model):
    alatid = models.ForeignKey('Alatberat', on_delete=models.CASCADE)
    tanggal = models.DateField(db_index=True, default=datetime.datetime.now)
    biaya = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=50, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return format(self.tanggal, "%d-%m-%Y")

    class Meta:
        verbose_name = 'Biaya / Service'
        verbose_name_plural = 'Biaya / Service'
        ordering = ['-tanggal']


# Historical based on alat berat
class Bbmab(models.Model):
    alatid = models.ForeignKey('Alatberat', on_delete=models.CASCADE)
    tanggal = models.DateField(db_index=True, default=datetime.datetime.now)
    hmnow = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="HM Saat ini")
    hmbefore = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="HM Sebelumnya")
    ltrmasuk = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Liter yg masuk")
    keterangan = models.CharField(max_length=50, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return format(self.tanggal, "%d-%m-%Y")

    class Meta:
        verbose_name = 'Input Pengisian BBM Alat'
        verbose_name_plural = 'Input Pengisian BBM Alat'
        ordering = ['-tanggal']
