# Generated by Django 2.2 on 2019-05-20 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['namasupplier'], 'verbose_name': 'Supplier', 'verbose_name_plural': 'Supplier'},
        ),
    ]