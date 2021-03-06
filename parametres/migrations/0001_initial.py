# Generated by Django 3.2.7 on 2021-09-30 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parametres.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=500, verbose_name='NATURE ACTIVITE')),
            ],
            options={
                'verbose_name': 'activite',
                'verbose_name_plural': 'ACTIVITES',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Campagne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(blank=True, editable=False, max_length=500, null=True)),
                ('mois_debut', models.CharField(choices=[('JAN', 'JANVIER'), ('FEV', 'FEVRIER'), ('MAR', 'MARS'), ('AVR', 'AVRIL'), ('MAI', 'MAI'), ('JUN', 'JUIN'), ('JUL', 'JUILLET'), ('AUG', 'AOUT'), ('SEP', 'SEPTEMBRE'), ('OCT', 'OCTOBRE'), ('NOV', 'NOVEMBRE'), ('DEC', 'DECEMBRE')], default='NOV', max_length=50)),
                ('annee_debut', models.IntegerField(choices=[(2019, 2019), (2020, 2020), (2021, 2021)], default=2021, verbose_name='Année début')),
                ('mois_fin', models.CharField(choices=[('JAN', 'JANVIER'), ('FEV', 'FEVRIER'), ('MAR', 'MARS'), ('AVR', 'AVRIL'), ('MAI', 'MAI'), ('JUN', 'JUIN'), ('JUL', 'JUILLET'), ('AUG', 'AOUT'), ('SEP', 'SEPTEMBRE'), ('OCT', 'OCTOBRE'), ('NOV', 'NOVEMBRE'), ('DEC', 'DECEMBRE')], default='SEP', max_length=50)),
                ('annee_fin', models.IntegerField(default=2022, verbose_name='Année fin')),
            ],
            options={
                'verbose_name': 'campagne',
                'verbose_name_plural': 'CAMPAGNES',
                'ordering': ['-titre'],
            },
        ),
        migrations.CreateModel(
            name='Cat_Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50, verbose_name='Categorie')),
            ],
            options={
                'verbose_name': 'categorie plant',
                'verbose_name_plural': 'CATEGORIES PLANTS',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Origine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, verbose_name='CODE PAYS')),
                ('pays', models.CharField(max_length=255, verbose_name='PAYS')),
            ],
            options={
                'verbose_name': 'origine',
                'verbose_name_plural': 'ORIGINES',
                'ordering': ['pays'],
            },
        ),
        migrations.CreateModel(
            name='Projet_Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=500, verbose_name='CATEGORIE PROJET')),
            ],
            options={
                'verbose_name': 'catégorie projet',
                'verbose_name_plural': 'CATEGORIES PROJETS',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'REGIONS',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Sous_Prefecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'sous prefecture',
                'verbose_name_plural': 'SOUS PREFECTURES',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigle', models.CharField(max_length=255)),
                ('titre', models.CharField(max_length=500)),
                ('chef', models.CharField(max_length=255)),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
                ('etat', models.CharField(choices=[('en_cours', 'EN COURS'), ('suspendu', 'SUSPENDU'), ('traite', 'TRAITE')], max_length=50)),
                ('categorie', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='parametres.projet_cat', verbose_name='CATEGORIE PROJET')),
            ],
            options={
                'verbose_name': 'projet',
                'verbose_name_plural': 'PROJETS',
                'ordering': ['sigle'],
            },
        ),
        migrations.CreateModel(
            name='Prime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('culture', models.CharField(choices=[('ANACARDE', 'ANACARDE'), ('CACAO', 'CACAO'), ('CAFE', 'CAFE'), ('COTON', 'COTON'), ('HEVEA', 'HEVEA'), ('PALMIER', 'PALMIER A HUILE')], max_length=150)),
                ('certification', models.CharField(choices=[('UTZ', 'UTZ'), ('RA', 'RA'), ('BIO', 'BIO'), ('PROJET', 'PROJET')], max_length=150)),
                ('prix', models.PositiveIntegerField(default=100, verbose_name='Prix/Kg')),
                ('campagne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.campagne')),
            ],
            options={
                'verbose_name': 'prime',
                'verbose_name_plural': 'PRIMES',
            },
        ),
        migrations.CreateModel(
            name='Espece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accronyme', models.CharField(max_length=250, verbose_name='NOM SCIENTIFIQUE')),
                ('libelle', models.CharField(max_length=250, verbose_name='NOM USUEL')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.cat_plant')),
            ],
            options={
                'verbose_name': 'espece',
                'verbose_name_plural': 'ESPECES',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siege', models.CharField(blank=True, max_length=255, null=True, verbose_name='SIEGE/LOCALITE')),
                ('sigle', models.CharField(max_length=500)),
                ('contacts', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, upload_to=parametres.models.upload_logo_site, verbose_name='logo')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cooperatives', to='clients.client')),
                ('projet', models.ManyToManyField(to='parametres.Projet')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cooperatives', to='parametres.region')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cooperatives', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'cooperative',
                'verbose_name_plural': 'COOPERATIVES',
                'ordering': ['sigle'],
            },
        ),
    ]
