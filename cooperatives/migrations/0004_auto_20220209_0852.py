# Generated by Django 3.1.7 on 2022-02-09 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperatives', '0003_auto_20220209_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='niveauformateur',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='NIVEAU ETUDE FORMATEUR'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='structureformateur',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='STRUCTURE FORMATEUR'),
        ),
    ]
