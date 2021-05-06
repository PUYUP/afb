# Generated by Django 2.2 on 2019-05-27 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbm', '0002_auto_20190522_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaksitangkiinduk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('masuk', models.DecimalField(decimal_places=2, max_digits=15)),
                ('keluar', models.DecimalField(decimal_places=2, max_digits=15)),
                ('keterangan', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('mobilid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbm.Mobiltangki')),
                ('tangkiid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbm.Tangkiinduk')),
            ],
            options={
                'verbose_name': 'Transaksi Tangki Induk',
                'verbose_name_plural': 'Transaksi Tangki Induk',
                'ordering': ['tanggal'],
            },
        ),
        migrations.CreateModel(
            name='Transaksimobiltangki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('keterangan', models.CharField(max_length=50)),
                ('masuk', models.DecimalField(decimal_places=2, max_digits=15)),
                ('keluar', models.DecimalField(decimal_places=2, max_digits=15)),
                ('mobilid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbm.Mobiltangki')),
                ('tangkiid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbm.Tangkiinduk')),
            ],
            options={
                'verbose_name': 'Transaksi Mobil Tangki',
                'verbose_name_plural': 'Transaksi Mobil Tangki',
                'ordering': ['tanggal'],
            },
        ),
    ]
