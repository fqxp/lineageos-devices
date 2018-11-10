# Generated by Django 2.1.3 on 2018-11-10 13:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ram_variants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=1, max_digits=10), size=None),
        ),
    ]