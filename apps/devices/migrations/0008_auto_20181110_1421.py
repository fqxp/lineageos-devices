# Generated by Django 2.1.3 on 2018-11-10 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_auto_20181110_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='screen_tech',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='sdcard',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='storage',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='tree',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='vendor',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='vendor_short',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
