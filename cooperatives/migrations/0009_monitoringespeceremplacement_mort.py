# Generated by Django 3.1.7 on 2022-02-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperatives', '0008_auto_20220210_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoringespeceremplacement',
            name='mort',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True, verbose_name='NOMBRE PLANTS MORT'),
        ),
    ]