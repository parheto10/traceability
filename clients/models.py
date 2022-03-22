# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import datetime

from django.utils.safestring import mark_safe
from django_countries.fields import CountryField

ANNEES = []
for r in range(2019, (datetime.datetime.now().year+1)):
    ANNEES.append((r,r))

def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.sigle + ".jpeg"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sigle = models.CharField(max_length=500, verbose_name="NOM / SIGLE")
    contacts = models.CharField(max_length=50, verbose_name="CONTACTS")
    libelle = models.CharField(max_length=250, verbose_name="NOM")
    pays = CountryField(blank_label='(Préciser Le Pays)')
    adresse = models.CharField(max_length=250, verbose_name="ADRESSE", blank=True)
    telephone1 = models.CharField(max_length=50)
    telephone2 = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, verbose_name="ADRESSE EMAIL")
    siteweb = models.CharField(max_length=120, blank=True, verbose_name="SITE WEB")
    logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % (self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.sigle = self.sigle.upper()
        self.libelle = self.libelle.upper()
        super(Client, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "CLIENTS"
        verbose_name = "client"

    def Logo(self):
        if self.logo:
            return mark_safe('<img src="%s" style="width: 60px; height:50px;" />' % self.logo.url)
        else:
            return "Aucun Logo"

    Logo.short_description = 'Logo'