# Generated by Django 2.0 on 2019-06-26 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbm', '0013_auto_20190626_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaksitangkiinduk',
            name='sisa',
        ),
    ]
