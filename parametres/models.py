# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import datetime
from django.db.models.deletion import CASCADE

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from clients.models import Client
#from cooperatives.models import Parcelle

ANNEES = []
for r in range(2019, (datetime.datetime.now().year+1)):
    ANNEES.append((r,r))

def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.code + ".jpeg"

ETAT = (
    ('en_cours', 'EN COURS'),
    ('suspendu', 'SUSPENDU'),
    ('traite', 'TRAITE'),
)

CULTURE = (
    ('ANACARDE', 'ANACARDE'),
    ('CACAO', 'CACAO'),
    ('CAFE', 'CAFE'),
    ('COTON', 'COTON'),
    ('HEVEA', 'HEVEA'),
    ('PALMIER', 'PALMIER A HUILE'),
)

CERTIFICATION = (
    ('UTZ', 'UTZ'),
    ('RA', 'RA'),
    ('BIO', 'BIO'),
    ('PROJET', 'PROJET'),
)

class Origine(models.Model):
    code = models.CharField(max_length=2, verbose_name="CODE PAYS")
    pays = models.CharField(max_length=255, verbose_name="PAYS")
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.pays)

    class Meta:
        verbose_name_plural = "ORIGINES"
        verbose_name = "origine"
        ordering = ["pays"]

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        self.pays = self.pays.upper()
        super(Origine, self).save(force_insert, force_update)

class Region(models.Model):
    libelle = models.CharField(max_length=250)
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.libelle)

    class Meta:
        verbose_name_plural = "REGIONS"
        verbose_name = "region"
        ordering = ["libelle"]

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Region, self).save(force_insert, force_update)

class Sous_Prefecture(models.Model):
    libelle = models.CharField(max_length=250)
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.libelle)

    class Meta:
        verbose_name_plural = "SOUS PREFECTURES"
        verbose_name = "sous prefecture"
        ordering = ["libelle"]

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Sous_Prefecture, self).save(force_insert, force_update)

class Projet_Cat(models.Model):
    libelle = models.CharField(max_length=500, verbose_name="CATEGORIE PROJET")
    objects = models.Manager()

    def __str__(self):
        return "%s" % (self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Projet_Cat, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "CATEGORIES PROJETS"
        verbose_name = "catégorie projet"
        ordering = ["libelle"]

class Projet(models.Model):
    # client = models.ForeignKey(Client, verbose_name="CLIENT", on_delete=models.CASCADE, default=1)
    categorie = models.ForeignKey(Projet_Cat, on_delete=models.CASCADE, verbose_name="CATEGORIE PROJET", default=1)
    sigle = models.CharField(max_length=255)
    titre = models.CharField(max_length=500)
    chef = models.CharField(max_length=255)
    debut = models.DateField()
    fin = models.DateField()
    etat = models.CharField(max_length=50, choices=ETAT)
    objects = models.Manager()

    def __str__(self):
        return "%s - (%s)" %(self.titre, self.categorie.libelle)

    class Meta:
        verbose_name_plural = "PROJETS"
        verbose_name = "projet"
        ordering = ["sigle"]

    def save(self, force_insert=False, force_update=False):
        self.sigle = self.sigle.upper()
        self.titre = self.titre.upper()
        self.chef = self.chef.upper()
        super(Projet, self).save(force_insert, force_update)

class Campagne(models.Model):
    Month_choice = (
        ('JAN', 'JANVIER'),
        ('FEV', 'FEVRIER'),
        ('MAR', 'MARS'),
        ('AVR', 'AVRIL'),
        ('MAI', 'MAI'),
        ('JUN', 'JUIN'),
        ('JUL', 'JUILLET'),
        ('AUG', 'AOUT'),
        ('SEP', 'SEPTEMBRE'),
        ('OCT', 'OCTOBRE'),
        ('NOV', 'NOVEMBRE'),
        ('DEC', 'DECEMBRE'),
    )
    titre = models.CharField(max_length=500, blank=True, null=True, editable=False)
    mois_debut = models.CharField(max_length=50, choices=Month_choice, default="NOV")
    annee_debut = models.IntegerField(verbose_name='Année début', choices=ANNEES, default=datetime.datetime.now().year)
    mois_fin = models.CharField(max_length=50, choices=Month_choice, default="SEP")
    annee_fin = models.IntegerField(verbose_name='Année fin', default=(datetime.datetime.now().year +1))

    class Meta:
        verbose_name_plural = "CAMPAGNES"
        verbose_name = "campagne"
        ordering = ["-titre"]

    def DEBUT(self):
        if self.mois_debut !="" and self.annee_debut !="":
            DEBUT = "%s, %s" %(self.mois_debut, self.annee_debut)
            return DEBUT

    def FIN(self):
        if self.mois_fin !="" and self.annee_fin !="":
            FIN = "%s, %s" %(self.mois_fin, self.annee_fin)
            return FIN

    def save(self, force_insert=False, force_update=False):
        if self.annee_fin =="":
            current_year  = datetime.datetime.now().year
            self.annee_fin = current_year + 1

        if self.mois_debut !="" and self.mois_fin !="" and self.annee_debut !="" and self.annee_fin !="" :
            self.titre = "%s,%s - %s,%s" %(self.mois_debut, self.annee_debut, self.mois_fin, self.annee_fin)
        super(Campagne, self).save(force_insert, force_update)

    def __str__(self):
        return "%s" %(self.titre)

class Prime(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=250)
    #certification = models.CharField(max_length=150, choices=CERTIFICATION)
    prix = models.PositiveIntegerField(default=100, verbose_name="Prix/Kg")
    objects = models.Manager()

    def __str__(self):
        return "%s-%s %s" %(self.libelle, self.prix)

    class Meta:
        verbose_name_plural = "PRIMES"
        verbose_name = "prime"

class Activite(models.Model):
    libelle = models.CharField(max_length=500, verbose_name="NATURE ACTIVITE")
    objects = models.Manager()

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Activite, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "ACTIVITES"
        verbose_name = "activite"
        ordering = ["libelle"]

class Cat_Plant(models.Model):
    libelle = models.CharField(max_length=50, verbose_name="Categorie")

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Cat_Plant, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "CATEGORIES PLANTS"
        verbose_name = "categorie plant"
        ordering = ["libelle"]

class Espece(models.Model):
    categorie = models.ForeignKey(Cat_Plant, on_delete=models.CASCADE)
    accronyme = models.CharField(max_length=250, verbose_name="NOM SCIENTIFIQUE")
    libelle = models.CharField(max_length=250, verbose_name="NOM USUEL")

    def __str__(self):
        return '%s (%s)' %(self.libelle, self.accronyme)

    def save(self, force_insert=False, force_update=False):
        self.accronyme = self.accronyme.upper()
        self.libelle = self.libelle.upper()
        super(Espece, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "ESPECES"
        verbose_name = "espece"
        ordering = ["libelle"]

class Cooperative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cooperatives")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cooperatives")
    siege = models.CharField(max_length=255, verbose_name="SIEGE/LOCALITE", blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="cooperatives")
    projet = models.ManyToManyField(Projet)
    sigle = models.CharField(max_length=500)
    contacts = models.CharField(max_length=50)
    logo = models.ImageField(verbose_name="logo", upload_to=upload_logo_site, blank=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('cooperatives:dashboard', kwargs={"id": self.id})

    def get_projet_values(self):
        ret = ''
        for proj in self.projet.all():
            ret = ret + proj.titre + ','
        return ret[:-1]

    def __str__(self):
        return '%s' %(self.sigle)

    def save(self, force_insert=False, force_update=False):
        self.sigle = self.sigle.upper()
        self.siege = self.siege.upper()
        self.user.last_name = self.user.last_name.upper()
        self.user.first_name = self.user.first_name.upper()
        super(Cooperative, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "COOPERATIVES"
        verbose_name = "cooperative"
        ordering = ["sigle"]

    def Logo(self):
        if self.logo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.logo.url)
        else:
            return "Aucun Logo"

    Logo.short_description = 'Logo'
    # Create your models here.

# Create your models here.


class ObsMonitoring(models.Model):
    libelle = models.CharField(max_length=255)


    def __str__(self):
        return '%s' % (self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(ObsMonitoring, self).save(force_insert, force_update)


class Pepiniere(models.Model):
    #cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=1)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, default=1)
    region = models.CharField(max_length=250, verbose_name="DELEGATION REGIONALE")
    ville = models.CharField(max_length=250, verbose_name="VILLE")
    site = models.CharField(max_length=250, verbose_name="SITE")
    latitude = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=10, null=True, blank=True)
    #fournisseur = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS FOURNISSEUR")
    #contacts_fournisseur = models.CharField(max_length=50, blank=True, null=True, verbose_name="CONTACTS FOURNISSEUR")
    technicien = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS TECHNICIEN")
    contacts_technicien = models.CharField(max_length=50, blank=True, null=True, verbose_name="CONTACTS TECHNICIEN")
    superviseur = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS TECHNICIEN")
    contacts_superviseur = models.CharField(max_length=50, blank=True, null=True, verbose_name="CONTACTS SUPERVISUER")
    sachet_recus = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SACHET RECU")
    production_plant = models.PositiveIntegerField(default=0, verbose_name="PLANTS A PRODUIRE")
    production_realise = models.PositiveIntegerField(default=0, verbose_name="REALISATION")
    pourcentage_prod = models.PositiveIntegerField(default=0, verbose_name="POURCENTAGE DE PRODUCTION")
    plant_mature = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANT MATURE")
    plant_retire = models.PositiveIntegerField(default=0, verbose_name="NBRE TOTAL PLANT RETIRE")
    # sachet_rempli = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SACHET REMPLI")
    # sachet_perdu = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SACHET PERDU")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - %s' %(self.ville, self.site)

    def taux(self):
        if self.production_plant != 0 and self.production_realise != 0:
            Taux = float("{:.2f}".format((self.production_realise / self.production_plant) * 100))
            self.pourcentage_prod = Taux
            return Taux

    def save(self, force_insert=False, force_update=False):
        self.region = self.region.upper()
        self.ville = self.ville.upper()
        self.site = self.site.upper()
        self.technicien = self.technicien.upper()
        self.superviseur = self.superviseur.upper()
        if self.production_plant !=0 and self.production_realise !=0:
            self.pourcentage_prod = float("{:.2f}".format((self.production_realise / self.production_plant) * 100))
        super(Pepiniere, self).save(force_insert, force_update)

    def coordonnees(self):
        return str(self.longitude) + ', ' + str(self.latitude)

    class Meta:
        verbose_name_plural = "PEPINIERES"
        verbose_name = "pépinière"
        # ordering = ["libelle"]




class DetailsSemenceEspece(models.Model):
    libelle = models.CharField(max_length=255)


    def __str__(self):
        return '%s' % (self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(DetailsSemenceEspece, self).save(force_insert, force_update)



class Fournisseur(models.Model):
    pseudo = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    localite = models.CharField(max_length=255)
    contact = models.CharField(max_length=255,verbose_name="CONTACT")
    objects = models.Manager()

    def __str__(self):
        return '%s - %s' % (self.pseudo,self.localite)

    def save(self, force_insert=False, force_update=False):
        self.pseudo = self.pseudo.upper()
        self.ville = self.ville.upper()
        self.localite = self.localite.upper()
        super(Fournisseur, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "FOURNISSEURS"
        verbose_name = "fournisseur"


class Semence_Pepiniere(models.Model):
    pepiniere = models.ForeignKey(Pepiniere, on_delete=models.CASCADE)
    espece_recu = models.ForeignKey(Espece, on_delete=models.CASCADE)
    production = models.PositiveIntegerField(default=0, verbose_name="NB PLANTS A PRODUIRE")
    qte_recu = models.PositiveIntegerField(default=0, verbose_name="QTE RECU")
    date = models.DateField(verbose_name="DATE RECEPTION")
    fournisseur = models.ForeignKey(Fournisseur,on_delete=CASCADE,blank=True,null=True)
    details = models.TextField(blank=True,null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def total_semence(self):
        pepiniere = get_object_or_404(Pepiniere, id=id)
        t_semence = Semence_Pepiniere.objects.filter(pepiniere_id=pepiniere).aggregate(total=Sum('qte_recu'))
        return t_semence

    class Meta:
        verbose_name_plural = "DETAILS SEMENCES RECUS"
        verbose_name = "détail semence reçu"
        # ordering = ["libelle"]


class Intitule_Formation(models.Model):
    libelle= models.CharField(max_length=255)
    projet = models.ForeignKey(Projet,on_delete=models.CASCADE)


    def __str__(self):
        return '%s - %s' % (self.libelle,self.projet)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Intitule_Formation, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "THEMES DES FORMATIONS"
        verbose_name = "theme formation"
    



class CampagneProduction(models.Model):
    libelle = models.CharField(max_length=250)
    annee = models.IntegerField(verbose_name='Année Campagne', choices=ANNEES, default=datetime.datetime.now().year)

    def __str__(self): 
        return '%s' %(self.libelle)










    

    





