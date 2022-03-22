
import datetime

import datetime
import os
import re
import sys
from numpy import iterable
from pandas import notnull

import requests
from django.conf import settings
from django.contrib.staticfiles import finders
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
# from django.contrib.gis.serializers import geojson
from django.core.serializers import serialize
from django.core import serializers
from django.http import HttpResponse, QueryDict
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import folium
from django_pandas.io import read_frame
from folium import raster_layers, plugins, Popup
import json
from django.template.loader import get_template, render_to_string
from django.views.generic import TemplateView
from folium.plugins import MarkerCluster
from rest_framework.decorators import api_view
from xhtml2pdf import pisa
from django.views import View
from xlrd.formatting import Format

# Import django Serializer Features #
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from parametres.forms import UserForm
from parametres.models import CampagneProduction, Intitule_Formation, Projet, Espece, Campagne
from parametres.serializers import ParcelleSerializer
from .forms import CoopForm, EditProductionForm, MonitoringEspeceForm, ParticipantcoopForm, ProdForm, EditProdForm, ParcelleForm, RemplacementMonitoringForm, SectionForm, Sous_SectionForm, \
     FormationForm, DetailFormation, EditFormationForm, EditParcelleForm, Edit_Sous_SectionForm, MonitoringForm, \
    PlantingForm, DetailPlantingForm, ProductionForm
from .models import Cooperative, DetailMonitoring, DetailPlantingRemplacement, MonitoringEspece, \
    MonitoringEspeceremplacement, Participantcoop, Participantformation, RemplacementMonitoring, Section, Sous_Section, \
    Producteur, Parcelle, Planting, Formation, Detail_Formation, \
    DetailPlanting, Monitoring, Production
from .serializers import CooperativeSerliazer, ParcelleSerliazer


def is_cooperative(user):
    return user.groups.filter(name='COOPERATIVES').exists()

#@login_required(login_url='connexion')
#@user_passes_test(is_cooperative)
# def cooperative(request, id=None):
#     coop = get_object_or_404(Cooperative, pk=id)
#     producteurs = Producteur.objects.all().filter(section__cooperative_id= coop)
#     nb_producteurs = Producteur.objects.all().filter(section__cooperative_id= coop).count()
#     parcelles = Parcelle.objects.all().filter(propietaire__section__cooperative_id=coop)
#     nb_parcelles = Parcelle.objects.all().filter(propietaire__section__cooperative_id=coop).count()
#     context = {
#         "coop": coop,
#         'cooperative': cooperative,
#         'producteurs': producteurs,
#         'nb_producteurs': nb_producteurs,
#         'parcelles': parcelles,
#         'nb_parcelles': nb_parcelles,
#     }
#     return render(request, "cooperatives/dashboard.html", context)

@login_required(login_url='connexion')
def coop_dashboard(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    producteurs = Producteur.objects.filter(cooperative_id=cooperative)
    nb_producteurs = Producteur.objects.filter(cooperative_id=cooperative, is_active=True).count()
    nb_formations = Formation.objects.all().filter(cooperative_id=cooperative).count()
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    nb_parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).count()
    Superficie = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    Plants = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('plant_total'))['total']
    section = Section.objects.all().filter(cooperative_id=cooperative)
    section_prod = Section.objects.annotate(nb_producteur=Count('producteurs'))
    section_parcelles = Parcelle.objects.filter(producteur__section_id__in=section).count()
    section_superf = Parcelle.objects.filter(producteur__section_id__in=section).aggregate(total=Sum('superficie'))['total']
    section_planting = DetailPlanting.objects.filter(planting__parcelle__producteur__section_id__in=section).aggregate(total=Sum('nb_plante'))['total']
    # detail_planting = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative)#.annotate(nb_plante=Sum('nb_plante'))
    espece_planting = Espece.objects.all()
    plantings = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plante'))['total']
    coop_plants = DetailPlanting.objects.filter(espece_id__in=espece_planting).aggregate(total=Sum('nb_plante'))['total']
    production = Production.objects.filter(parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('qteProduct'))['total']
    petite_production = Production.objects.filter(parcelle__producteur__cooperative_id=cooperative).filter(campagne="petite").aggregate(total=Sum('qteProduct'))['total']
    grande_production = Production.objects.filter(parcelle__producteur__cooperative_id=cooperative).filter(campagne="grande").aggregate(total=Sum('qteProduct'))['total']
    # plantings = DetailPlanting.objects.values("espece__libelle").filter(planting__parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plante'))['total']
    # print(plantings)
    # espece_planting = DetailPlanting.objects.filter(espece__libelle__in=details_planting).aggregate(total=Sum('nb_plante'))['total']
    # espece_planting = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).annotate(nb_plante=Sum('nb_plante'))
    # print(section_prod)
    # nb_producteurs = sections.producteur.set_all()
    # querysets = Detail_Retrait_plant.objects.values("espece__libelle").filter(retait__pepiniere__cooperative_id=cooperative).annotate(plant_retire=Sum('plant_retire'))
    # semences = Semence_Pepiniere.objects.values("espece_recu__libelle").filter(pepiniere__cooperative_id=cooperative).annotate(qte_recu=Sum('qte_recu'))
    activate = "cooperative"
    context={
    'cooperative':cooperative,
    'producteurs': producteurs,
    'nb_producteurs': nb_producteurs,
    'nb_formations': nb_formations,
    'section_prod': section_prod,
    'section_parcelles': section_parcelles,
    'section_superf': section_superf,
    'parcelles': parcelles,
    'nb_parcelles': nb_parcelles,
    'Superficie' : Superficie,
    'Plants': Plants,
    'section': section,
    'section_planting': section_planting,
    'espece_planting': espece_planting,
    'plantings': plantings,
    'coop_plants': coop_plants,
    'production': production,
    'petite_production': petite_production,
    'grande_production': grande_production,
    'activate':activate
    # 'labels': labels,
    # 'data': data,
    # 'mylabels': mylabels,
    # 'mydata': mydata,
    }
    return render(request, 'cooperatives/dashboard.html', context=context)

def coopdetailPlantings(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    querysets = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).values("espece__libelle").annotate(nb_plante=Sum('nb_plante'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['espece__libelle'])
        data.append(stat['nb_plante'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

# def prod_section(request):
#     cooperative = Cooperative.objects.get(user_id=request.user.id)
#     semences = Semence_Pepiniere.objects.values("espece_recu__libelle").filter(pepiniere__cooperative_id=cooperative).annotate(qte_recu=Sum('qte_recu'))
#     labels = []
#     data = []
#     for stat in semences:
#         labels.append(stat['espece_recu__libelle'])
#         data.append(stat['qte_recu'])
#
#     return JsonResponse(data= {
#         'labels':labels,
#         'data':data,
#     })

@login_required(login_url='connexion')
def add_section(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    sections = Section.objects.all().filter(cooperative_id=cooperative)
    form = SectionForm()
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cooperative_id = cooperative.id
            section = section.save()
            # print()
        messages.success(request, "Section Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:section'))
    context = {
        "cooperative": cooperative,
        "sections": sections,
        'form': form,
    }
    return render(request, "cooperatives/sections.html", context)



def delete_section(request, id=None):
    item = get_object_or_404(Section, id=id)
    if request.method == "POST":
        item.delete()
        messages.error(request, "Section Supprimée Avec Succès")
        return redirect('cooperatives:section')
    context = {
        # 'pepiniere': pepiniere,
        'item': item,
    }
    return render(request, 'cooperatives/section_delete.html', context)
    # item.delete()
    # messages.success(request, "Section Supprimer avec Succès")
    # return HttpResponseRedirect(reverse('cooperatives:section'))

@login_required(login_url='connexion')
def add_sous_section(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    sections = Section.objects.all().filter(cooperative_id=cooperative)
    sous_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)
    form = Sous_SectionForm()
    if request.method == 'POST':
        form = Sous_SectionForm(request.POST)
        if form.is_valid():
            sous_section = form.save(commit=False)
            sous_section = sous_section.save()
        messages.success(request, "Sous Section Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:sous_sections'))
    context = {
        "cooperative": cooperative,
        "sous_sections": sous_sections,
        "sections": sections,
        'form': form,
    }
    return render(request, "cooperatives/sous_sections.html", context)





def my_section(request):
    cooperative = request.GET.get("user_id")#Cooperative.objects.get(user_id=request.user.id)
    coop_sections = Section.objects.filter(cooperative_id=cooperative)
    context = {'coop_sections': coop_sections}
    return render(request, 'cooperatives/section.html', context)


@login_required(login_url='connexion')
def producteurs(request):
    activate = "producteurs"
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    producteurs = Producteur.objects.filter(cooperative_id=cooperative)#.order_by("-add_le")
    sections = Section.objects.filter(cooperative_id=cooperative)
    sous_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)

    prodForm = ProdForm()
   # if request.method == 'POST':
   #     prodForm = ProdForm(request.POST, request.FILES)
   #    
   #     if prodForm.is_valid():
   #         producteur = prodForm.save(commit=False)
   #         producteur.cooperative_id = cooperative.id
   #         
   #         producteur = producteur.save()
   #         # print(producteur)
   #         messages.success(request, "Producteur Ajouté avec succès")
   #         return HttpResponseRedirect(reverse('cooperatives:producteurs'))

    context = {
        "cooperative":cooperative,
        "producteurs": producteurs,
        'prodForm': prodForm,
        'sections':sections,
        'sous_sections':sous_sections,
        'activate':activate

    }
    return render(request, "cooperatives/producteurs.html", context)

#def prod_update(request, code=None):
#	instance = get_object_or_404(Producteur, code=code)
#	form = EditProdForm(request.POST or None, request.FILES or None, instance=instance)
#	if form.is_valid():
#		instance = form.save(commit=False)
#		instance.save()
#		messages.success(request, "Producteur Modifié Avec Succès", extra_tags='html_safe')
#		return HttpResponseRedirect(reverse('cooperatives:producteurs'))
#
#	context = {
#		"instance": instance,
#		"form":form,
#	}
#	return render(request, "cooperatives/prod_edt.html", context)
    

def prod_delete(request, code=None):
    item = get_object_or_404(Producteur, code=code)
    item.delete()


@login_required(login_url='connexion')
def parcelles(request):
    activate = "parcelles"
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    prods = Producteur.objects.filter(cooperative_id=cooperative)
    s_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    parcelleForm = ParcelleForm(request.POST or None)
    if request.method == 'POST':
        parcelleForm = ParcelleForm(request.POST, request.FILES)
        if parcelleForm.is_valid():
            parcelle = parcelleForm.save(commit=False)
            for prod in prods:
                parcelle.producteur_id = prod.id
                if not parcelle.code:
                    tot = Parcelle.objects.filter(producteur_id=prod).count()
                    parcelle.code = "%s-%s" % (parcelle.producteur.code, tot)

            for sect in s_sections:
                parcelle.sous_section_id = sect.id

            parcelle = parcelle.save()
        messages.success(request, "Parcelle Ajoutés avec succès")
        return HttpResponseRedirect(reverse('cooperatives:parcelles'))

    context = {
        "cooperative":cooperative,
        "parcelles": parcelles,
        'parcelleForm': parcelleForm,
        'producteurs': prods,
        's_sections': s_sections,
        'activate': activate
    }
    return render(request, "cooperatives/parcelles.html", context)



def parcelle_delete(request, id=None):
    parcelle = get_object_or_404(Parcelle, id=id)
    parcelle.delete()


def detail_parcelles(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    plantings = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative)
    instance = get_object_or_404(Planting, id=id)
    # details = Details_planting.objects.all().filter(planting_id=instance)

    context = {

    }

    return render(request, 'cooperatives/detail_parcelle', context)


# def planting(request):
#     cooperative = Cooperative.objects.get(user_id=request.user.id)
#     # producteurs = Producteur.objects.all().filter(cooperative=cooperative)
#     parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
#     plantings = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative)
#     plantingForm = PlantingForm()
#     if request.method == 'POST':
#         plantingForm = PlantingForm(request.POST, request.FILES)
#         if plantingForm.is_valid():
#             planting = plantingForm.save(commit=False)
#             for parcelle in parcelles.iterator():
#                 planting.parcelle_id = parcelle.id
#             planting = planting.save()
#             print(planting)
#             # print(planting.parcelle.producteur)
#         messages.success(request, "Parcelle Ajoutés avec succès")
#         return HttpResponseRedirect(reverse('cooperatives:planting'))
#     context = {
#         "cooperative":cooperative,
#         "parcelles": parcelles,
#         "plantings": plantings,
#         'plantingForm': plantingForm,
#     }
#     return render(request, "cooperatives/plantings.html", context)

# def suivi_planting(request, id=None):
#     instance = get_object_or_404(Planting, id=id)
#     # details = Details_planting.objects.all().filter(planting_id=instance)
#
#     # suiviForm = SuiviPlantingForm()
#     # if request.method == 'POST':
#     #     suiviForm = SuiviPlantingForm(request.POST, request.FILES)
#     #     if suiviForm.is_valid():
#     #         suivi = suiviForm.save(commit=False)
#     #         suivi.planting_id = instance.id
#     #         suivi = suivi.save()
#     #         print(suivi)
#     #     messages.success(request, "Planting Ajouté avec succès")
#     #     return HttpResponseRedirect(reverse('cooperatives:planting'))
#     # context = {
#     #     'instance':instance,
#     #     'details':details,
#     #     'suiviForm':suiviForm,
#     # }
#     # return render(request, 'cooperatives/suivi_planting.html', context)

# def planting_update(request, id=None):
# 	instance = get_object_or_404(Planting, id=id)
# 	# form = PlantingForm(request.POST or None, request.FILES or None, instance=instance)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		messages.success(request, "Modification effectuée avec succès")
# 		return HttpResponseRedirect(reverse('cooperatives:planting'))
#
# 	context = {
# 		"instance": instance,
# 		"form":form,
# 	}
# 	return render(request, "cooperatives/planting_edit.html", context)

#-------------------------------------------------------------------------
## Export to Excel
#-------------------------------------------------------------------------

import csv

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_producteur_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="producteurs.csv"'

    writer = csv.writer(response)
    writer.writerow(['CODE', 'TYPE', 'SECTION', 'GENRE', 'NOM', 'PRENOMS', 'CONTACTS'])
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    # producteurs = Producteur.objects.all().filter(cooperative=cooperative)

    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'code',
        'type_producteur',
        'section__libelle',
        'genre',
        'nom',
        'prenoms',
        'contacts',
    )
    for p in producteurs:
        writer.writerow(p)

    return response

import xlwt

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_prod_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producteurs')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['CODE', 'NOM ET PRENOMS', 'SECTION', 'LOCALITE', 'TYPE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'code',
        'nom',
        'section__libelle',
        'localite',
        'type_producteur',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_planting_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producteurs')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['CODE', 'PRODUCTEUR', 'SECTION', 'ESPECE', 'QTE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = DetailPlanting.objects.all().filter(planting__parcelle__producteur__cooperative_id=cooperative.id).values_list(
        'planting__parcelle__code',
        'planting__parcelle__producteur__nom',
        'planting__parcelle__producteur__section__libelle',
        'espece__libelle',
        'nb_plante',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_section_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sections.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sections')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['LIBELLE', 'RESPONSABLE', 'CONTACTS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Section.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'libelle',
        'responsable',
        'contacts',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_sous_section_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sous Sections.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sous Sections')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['SECTION', 'LIBELLE', 'RESPONSABLE', 'CONTACTS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Sous_Section.objects.all().filter(section__cooperative_id=cooperative.id).values_list(
        'section__libelle',
        'libelle',
        'responsable',
        'contacts',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_parcelle_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Parcelles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Parcelles')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['CODE', 'PRODUCETUR', 'SECTION', 'SUPER', 'LONG', 'LAT', 'CULTURE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative.id).values_list(
        'code',
        'producteur__nom',
        'producteur__section__libelle',
        'superficie',
        'longitude',
        'latitude',
        'culture',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_formation_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Formations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Formations')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['PROJET', 'FORMATEUR', 'INTITULE', 'DEBUT', 'FIN']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    # format2 = xlwt.Workbook({'num_format': 'dd/mm/yy'})
    rows = Formation.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'projet__titre',
        'formateur',
        'libelle',
        'debut',
        'fin',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                DEBUT = row[col_num].strftime('%d/%m/%Y')
                FIN = row[col_num].strftime('%d/%m/%Y')
                ws.write(row_num, col_num, DEBUT, FIN, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
            # ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_plant_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Planting.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Plants')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['P.CODE', 'P.NOM', 'P.PRENOMS', 'PARCELLE', 'ESPECE', 'NOMBRE', 'DATE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Planting.objects.all().filter(parcelle__propietaire__cooperative_id=cooperative.id).values_list(
        'parcelle__propietaire__code',
        'parcelle__propietaire__nom',
        'parcelle__propietaire__prenoms',
        'parcelle__code',
        'espece',
        'nb_plant',
        'date',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_prod_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Producteurs.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse

def localisation(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    # section = Section.objects.all().filter(cooperative_id=cooperative)
    sections = Section.objects.all().filter(cooperative_id=cooperative) #Parcelle.objects.filter(producteur__section_id__in=section)
    context = {
        'cooperative': cooperative,
        'parcelles' : parcelles,
        'sections' : sections
    }
    return render(request, 'cooperatives/carte_update.html', context)


@login_required(login_url='connexion')
def formation(request):
    activate = "formations"
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    themes = Intitule_Formation.objects.all()  

    context = {
        'cooperative': cooperative,
        'themes': themes,
        'activate': activate
    }
    return render(request, 'cooperatives/formations.html', context)

def Editformation(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Formation, id=id)
    form = EditFormationForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.cooperative_id = cooperative.id
        instance.save()
        instance.save()
        messages.success(request, "Modification Effectuée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:formations'))

    context = {
        "cooperative":cooperative,
        "instance": instance,
        "form": form,
    }
    return render(request, "cooperatives/edit_formation.html", context)

# def detail_formation(request, id=None):
#     cooperative = Cooperative.objects.get(user_id=request.user.id)
#     # instance = Detail_Formation.objects.get(formation_id=id)
#     instance = get_object_or_404(Formation, id=id)
#     details = Detail_Formation.objects.all().filter(formation_id=instance)
#     participants = Producteur.objects.all().filter(cooperative_id=cooperative)
#     form = DetailFormation()
#     if request.method == 'POST':
#         form = DetailFormation(request.POST, request.FILES)
#         if form.is_valid():
#             detail = form.save(commit=False)
#             detail.formation_id = instance.id
#             # for p in participants:
#                 # detail.
#             detail = detail.save()
#             # print(detail)
#             # print(planting.parcelle.producteur)
#         messages.success(request, "Formation Ajoutée avec succès")
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         # return HttpResponseRedirect(reverse('cooperatives:formations'))
#     # participants = Producteur.objects.all().filter(formation_id=formation)
#     context = {
#         'instance': instance,
#         'details': details,
#         'form': form,
#         'participants': participants,
#     }
#     return render(request, 'cooperatives/detail_formation.html', context)

@login_required(login_url='connexion')
def detail_formation(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    theme = get_object_or_404(Intitule_Formation, id=id)
    formations = Formation.objects.filter(intitule_id = theme.id,cooperative_id=cooperative.id)

  

    for formation in formations :
        formation.nb_participant = Participantformation.objects.filter(formation_id = formation.id).count()



    context = {
        'theme': theme,
        'formations':formations,
        'cooperative':cooperative
    }

    
    return render(request, 'cooperatives/detail_formation.html', context)

#Parcelle Json
# def my_parcelles(request):
#     parcelles = Parcelle.objects.all()
#     parcelles_list = serializers.serialize('json', parcelles)
#     return HttpResponse(parcelles_list, content_type="text/json-comment-filtered")

# class ParcellesView(View):
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             parcelles = Producteur.objects.all()
#             parcelles_serializers = serializers.serialize('json', parcelles)
#             return JsonResponse(parcelles_serializers, safe=False)
#         return JsonResponse({'message': 'Erreure Lors du Chargement.....'})
    # parcelles = Parcelle.objects.all()
    # parcelles_list = serializers.serialize('json', parcelles)
    # return HttpResponse(parcelles_list, content_type="text/json-comment-filtered")

# DJango Serializer Views#

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path
#Export PARCELLES to PDF
@login_required(login_url='connexion')
def export_prods_to_pdf(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    template_path = 'cooperatives/producteurs_pdf.html'
    context = {
        'cooperative':cooperative,
        'producteurs':producteurs,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Liste Producteur.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')
    return response


def export_parcelles_to_pdf(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    template_path = 'cooperatives/new_parcelles_pdf.html'
    context = {
        'cooperative': cooperative,
        'parcelles': parcelles,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Liste Producteur.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')
    return response

@csrf_exempt
def parcelle_list(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
        parcelles_serializers = serializers.serialize('json', parcelles)
        return JsonResponse(parcelles_serializers, safe=False)

class ParcellesMapView(TemplateView):

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["parcelles_coop"] = json.loads(serialize("geojson", Parcelle.objects.all()))
        # parcelles_serializers = serializers.serialize('json', parcelles)
        # context["parcelles"] = json.loads(serialize("geojson", Parcelle.objects.all()))
        return context

class ReceptionView(View):
    def get(self, request, *args, **kwargs):
        cooperative = Cooperative.objects.get(user_id=request.user.id)
        parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
        parcelle_list = []
        for parcelle in parcelles:
        #     sub_category = SubCategories.objects.filter(is_active=1, category_id=category.id)
            parcelle_list.append({"parcelle": parcelle})

        # merchant_users = MerchantUser.objects.filter(auth_user_id__is_active=True)
        especes_plants = Espece.objects.all()
        context = {
            "parcelles": parcelles,
            "especes_plants" : especes_plants,
        }
        return render(self.request, "cooperatives/planting_create.html", context)


class AddPlantingView(View):
    def get(self, request, *args, **kwargs):
        cooperative = Cooperative.objects.get(user_id=request.user.id)
        parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
        parcelle_list = []
        for parcelle in parcelles:
            parcelle_list.append({"parcelle": parcelle})

        # merchant_users = MerchantUser.objects.filter(auth_user_id__is_active=True)
        #activate = "plantings"
        especes = Espece.objects.all()
        print(especes)
        campagnes = Campagne.objects.all()
        projets = Projet.objects.all()
        plantings = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
        context = {
            'cooperative': cooperative,
            "parcelles": parcelles,
            "campagnes" : campagnes,
            "projets" : projets,
            "especes" : especes,
            "plantings" : plantings,
            #"activate": activate
        }
        return render(self.request, "cooperatives/plantings.html", context)

    def post(self, request, *args, **kwargs):
        cooperative = request.POST.get('cooperative')
        date = request.POST.get("date")
        nb_plant_exitant = request.POST.get("nb_plant_exitant")
        plant_recus = request.POST.get("plant_recus")
        # details = request.POST.get("details")
        campagne = request.POST.get("campagne")
        parcelle = request.POST.get("parcelle")
        projet = request.POST.get("projet")
        espece_list = request.POST.get("espece")
        nb_plante_liste = request.POST.getlist("nb_plante[]")

        parcelle_obj = Parcelle.objects.get(id=parcelle)
        campagne_obj = Campagne.objects.get(id=campagne)
        projet_obj = Projet.objects.get(id=projet)
        plant_total_obj = nb_plant_exitant + plant_recus

        planting = Planting(
            parcelle=parcelle_obj,
            campagne=campagne_obj,
            projet=projet_obj,
            nb_plant_exitant=nb_plant_exitant,
            plant_recus=plant_recus,
            date=date,
            # plant_recus = (nb_plant_exitant + plant_recus)
        )
        planting.save()


        # espece_obj = Espece.objects.get(id=espece_list)
        # detail_planting = DetailPlanting(
        #     planting_id=planting,
        #     espece = espece_obj,
        #     nb_plante=nb_plante_liste[i]
        # )
        # detail_planting.save()
        # i = i + 1
        # i = 0
        # # espece_obj = Espece.objects.get(id=espece_list)
        # for e in espece_list:
        #     detail_planting = DetailPlanting(
        #         planting_id=planting,
        #         espece=e,
        #         nb_plante=nb_plante_liste[i]
        #     )
        #     detail_planting.save()
        #     i = i+1
        # return HttpResponse("OK")

# def load_producteurs(request):
#     cooperative = Cooperative.objects.get(user_id=request.user.id)
#     producteurs = Producteur.objects.filter(cooperative_id=cooperative).order_by('nom')
#     parcelles = Parcelle.objects.filter(producteur__cooperative_id=cooperative)
#     context = {
#         'producteurs': producteurs,
#         'parcelles': parcelles,
#     }
#     return render(request, 'cooperative/select.html', context)

@login_required(login_url='connexion')
def CoopPlantings(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    # parcelles = cooperative.parcelles_set.all()
    parcelles = Parcelle.objects.filter(producteur__cooperative_id=cooperative)
    #print(parcelles)
    especes  = Espece.objects.all()
    activate = "plantings"
    # especes = Espece.objects.all()
    campagnes = Campagne.objects.all()
    projets = Projet.objects.all()
    plantings = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    plantingForm = PlantingForm()


    context = {
        'cooperative':cooperative,
        'parcelles':parcelles,
        'plantings':plantings,
        'campagnes':campagnes,
        'projets':projets,
        'especes': especes,
        'plantingForm':plantingForm,
        "activate": activate
    }
    return render(request, 'cooperatives/plantings.html', context)

@login_required(login_url='connexion')
def detail_planting(request, id=None):
    activate = "plantings"
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Planting, id=id)
    Details_Planting = DetailPlanting.objects.filter(planting_id=instance)
    
    Monitorings = Monitoring.objects.filter(planting_id=instance)
    remplacements = RemplacementMonitoring.objects.filter(monitoring__planting_id = instance.id)

    for remp in remplacements :
        remp.mort = MonitoringEspeceremplacement.objects.filter(remplacement_id = remp.id).aggregate(total=Sum('mort'))['total']
        remp.remplacer = MonitoringEspeceremplacement.objects.filter(remplacement_id = remp.id).aggregate(total=Sum('remplacer'))['total']
        #print(remp.mort)

    for monitoring in Monitorings:
        try:
            monitoring.remplacer = RemplacementMonitoring.objects.filter(monitoring_id = monitoring.id).latest('id')        
            
        except RemplacementMonitoring.DoesNotExist:
            pass
        
 

    monitoringForm = MonitoringForm()
    detailPlantingForm = DetailPlantingForm()

    if request.method == 'POST':

        monitoringForm = MonitoringForm(request.POST, request.FILES)
        detailPlantingForm = DetailPlantingForm(request.POST, request.FILES)

        if monitoringForm.is_valid():
            monitoring = monitoringForm.save(commit=False)
            monitoring.planting_id = instance.id
            monitoring = monitoring.save()            
            monitoringForm.save_m2m()
    
            #print(monitoring)
            messages.success(request, "Enregistrement effectué avec succès")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return HttpResponse("Enregistrement effectué avec succès")

        elif detailPlantingForm.is_valid():
            detail = detailPlantingForm.save(commit=False)
            detail.planting_id = instance.id
            detail = detail.save()
            print(detail)
            messages.success(request, "Enregistrement effectué avec succès")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('cooperatives:suivi_planting', kwargs={'cooperatives:suivi_planting': instance.pk})
            # return HttpResponse("Enregistrement effectué avec succès")
        else:
            pass


    
    try:
        lastMonitoring = Monitoring.objects.filter(planting_id=instance).latest('id')
        context = {
            'cooperative':cooperative,
            'instance':instance,
            'monitoringForm':monitoringForm,
            'detailPlantingForm':detailPlantingForm,
            'Details_Planting':Details_Planting,
            'Monitorings':Monitorings,
            "activate": activate,
            "lastMonitoring":lastMonitoring,
            "remplacements":remplacements
        
       
         }
        

    except Monitoring.DoesNotExist:
             context = {
            'cooperative':cooperative,
            'instance':instance,
            'monitoringForm':monitoringForm,
            'detailPlantingForm':detailPlantingForm,
            'Details_Planting':Details_Planting,
            'Monitorings':Monitorings,
            "activate": activate,
            "remplacements":remplacements
        
       
         }

    return render(request, 'cooperatives/detail_planting.html', context)
   
    


from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import DetailPlantingFormSet
from .models import Planting


class PlantingList(ListView):
    model = Planting
    template_name = "cooperatives/plantings.html"


# class PlantingCreate(CreateView):
#     model = Planting
#     fields = [
#         "parcelle",
#         "nb_plant_exitant",
#         "plant_recus",
#         "campagne",
#         "projet",
#         "date",
#         "date",
#         "details",
#     ]
#
#
# class PlantingDetailsCreate(CreateView):
#     model = Planting
#     fields = [
#         "parcelle",
#         "nb_plant_exitant",
#         "plant_recus",
#         "campagne",
#         "projet",
#         "date",
#         "date",
#         "details",
#     ]
#     success_url = reverse_lazy('add_planting')
#
#     def get_context_data(self, **kwargs):
#         data = super(PlantingDetailsCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['detailsplanting'] = DetailPlantingFormSet(self.request.POST)
#         else:
#             data['detailsplanting'] = DetailPlantingFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         detailsplanting = context['detailsplanting']
#         with transaction.atomic():
#             self.object = form.save()
#
#             if detailsplanting.is_valid():
#                 detailsplanting.instance = self.object
#                 detailsplanting.save()
#         return super(PlantingDetailsCreate, self).form_valid(form)


# class ProfileUpdate(UpdateView):
#     model = Profile
#     success_url = '/'
#     fields = ['first_name', 'last_name']
#
#
# class ProfileFamilyMemberUpdate(UpdateView):
#     model = Profile
#     fields = ['first_name', 'last_name']
#     success_url = reverse_lazy('profile-list')
#
#     def get_context_data(self, **kwargs):
#         data = super(ProfileFamilyMemberUpdate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['familymembers'] = FamilyMemberFormSet(self.request.POST, instance=self.object)
#         else:
#             data['familymembers'] = FamilyMemberFormSet(instance=self.object)
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         familymembers = context['familymembers']
#         with transaction.atomic():
#             self.object = form.save()
#
#             if familymembers.is_valid():
#                 familymembers.instance = self.object
#                 familymembers.save()
#         return super(ProfileFamilyMemberUpdate, self).form_valid(form)


# class PlantingDelete(DeleteView):
#     model = Planting
#     success_url = reverse_lazy('add_planting')


def folium_map(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)

    m = folium.Map(
        location=[5.34939, -4.01705],
        zoom_start=6
    )
    marker_cluster = MarkerCluster().add_to(m)

    map1 = raster_layers.TileLayer(tiles="CartoDB Dark_Matter").add_to(m)
    map2 = raster_layers.TileLayer(tiles="CartoDB Positron").add_to(m)
    map3 = raster_layers.TileLayer(tiles="Stamen Terrain").add_to(m)
    map4 = raster_layers.TileLayer(tiles="Stamen Toner").add_to(m)
    map5 = raster_layers.TileLayer(tiles="Stamen Watercolor").add_to(m)
    folium.LayerControl().add_to(m)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    df = read_frame(parcelles,
                        fieldnames=
                        [
                            'code',
                            'producteur',
                            'sous_section',
                            'acquisition',
                            'latitude',
                            'longitude',
                            'superficie',
                            'culture',
                            'certification',
                        ]
                    )
    # print(df)
    for (index, row) in df.iterrows():
        folium.Marker(
            location=[
                row.loc['latitude'],
                row.loc['longitude']
            ],
           # my_string='CODE: {}, PRODUCTEUR: {}, SECTION: {}, CERTIFICATION: {}, CULTURE: {}, SUPERFICIE: {}'.format(code,),
            # Popup(my_string),
            popup=[
                row.loc['code'],
                row.loc['producteur'],
                row.loc['certification'],
                row.loc['superficie'],
                row.loc['culture'],
                # 'producteur',
                # 'code',
                # 'certification',
                # 'culture',
                # 'superficie',
                # 'CODE' : 'code',
                # 'PRODUCTUER' : 'producteur',
                # 'SOUS SECTION' : 'sous_section',
                # 'CERTIFICATION' : 'certification',
                # 'CULTURE' : 'culture',
                # 'SUPERFICIE' : 'superficie',
            ],
            icon=folium.Icon(color="green", icon="ok-sign"),
        ).add_to(marker_cluster)
    plugins.Fullscreen().add_to(m)
    plugins.DualMap().add_to(m)
    # plugins.MarkerCluster.add_to()
    m = m._repr_html_()

    context = {
        "m":m
    }
    return render(request, "cooperatives/folium_map.html", context)

def folium_palntings_map(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    m = folium.Map(
        location=[5.34939, -4.01705],zoom_start=6,
    )
    marker_cluster = MarkerCluster().add_to(m)

    map1 = raster_layers.TileLayer(tiles="CartoDB Dark_Matter").add_to(m)
    map2 = raster_layers.TileLayer(tiles="CartoDB Positron").add_to(m)
    map3 = raster_layers.TileLayer(tiles="Stamen Terrain").add_to(m)
    map4 = raster_layers.TileLayer(tiles="Stamen Toner").add_to(m)
    map5 = raster_layers.TileLayer(tiles="Stamen Watercolor").add_to(m)
    folium.LayerControl().add_to(m)
    plantings = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative)
    parcelles = Parcelle.objects.filter(roducteur__cooperative_id=cooperative)

    df1 = read_frame(parcelles,
        fieldnames=
        [
            'code',
            'producteur',
            'latitude',
            'longitude',

        ]
    )
    df = read_frame(plantings,
        fieldnames=
        [
            'planting',
            'espece',
            'nb_plante',
            'add_le'
        ]
    )
    print(df)
    html = df.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )

    # print(df)
    for (index, row) in df1.iterrows():
        folium.Marker(
            location=[
                row.loc['latitude'],
                row.loc['longitude']
            ],
            popup=folium.Popup(html),
            icon=folium.Icon(color="green", icon="ok-sign"),
        ).add_to(marker_cluster)
    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        "m":m
    }
    return render(request, "cooperatives/folium_planting_map.html", context)


@api_view(['GET'])
def getParcelleCoop(request, pk=None):
    cooperative = Cooperative.objects.get(id=pk)
    # cooperative = Cooperative.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.filter(producteur__cooperative_id=cooperative)
    serializer = ParcelleSerializer(parcelles, many=False)
    # serializer = CooperativeSerliazer(cooperative, many=False)
    return Response(serializer.data)


 
#parcelle par cooperative sur la carte

@api_view(['GET'])
def map_by_cooperative(request):
    coop_connect = Cooperative.objects.get(user_id=request.user.id)
    sections  = Section.objects.filter(cooperative_id = coop_connect.id)
    context = {
        "coop_connect":coop_connect,
        "sections": sections
    }

    return render(request, 'cooperatives/usercoop/coop_connect_carte.html',context)


#EN MAINTENANCE
@api_view(['GET'])
def edit_monitoring_view(request,id=None): 
    d_date = 1
    monitoring = get_object_or_404(Monitoring, id=id)
    detail_monitoring = get_object_or_404(DetailMonitoring, monitoring_id=id)
    especemonitoring = MonitoringEspece.objects.filter(detailmonitoring_id = detail_monitoring.id)
    monitoringForm = MonitoringForm(request.POST or None, request.FILES or None, instance=monitoring)
    context = {
        "monitoring":monitoring,
        "detail_monitoring":detail_monitoring,
        "monitoringForm": monitoringForm,
        "d_date":d_date,
        "Plantings":especemonitoring
    }
    
    templateStr = render_to_string("cooperatives/edit_monitoring.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)



@api_view(['POST'])
def edit_monitoring(request):
    monitoring_id = request.POST['monitoring_id']
    detail_monitoring = request.POST['detailmonitoring_id']
    instance = get_object_or_404(Monitoring, id=monitoring_id)
    

    monitoringForm = MonitoringForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if monitoringForm.is_valid():
            monitoring = monitoringForm.save(commit=False)
            monitoring.save()
            monitoringForm.save_m2m()

            espece = request.POST.getlist('espece')
            detailplanting = request.POST.getlist('d_planting')
            mort = request.POST.getlist('mort')
            mature = request.POST.getlist('mature')
           #print(espece,detailplanting,mort,mature)
           
            tot_mature = 0
            tot_mort = 0
            for es,de,mt,mtr in zip(espece,detailplanting,mort,mature):
                MonitoringEspece.objects.create(espece_id = int(es),detailplanting_id = int(de),mort=int(mt),mature =int(mtr) ,  detailmonitoring_id = detail_monitoring)
                MonitoringEspece.objects.filter(detailmonitoring_id = detail_monitoring).delete()
                tot_mature = tot_mature + int(mtr)
                tot_mort = tot_mort + int(mt)

            monitoring.mature_global = tot_mature
            monitoring.mort_global = tot_mort
            monitoring.save()
            
            return JsonResponse({"msg": "Modification effectuée avec success","status":200},safe=False)
        else:
            return JsonResponse({"errors":monitoringForm.errors,"danger": "Modification incorrect"},safe=False)
        
#FIN DE EN MAINTENANCE


@api_view(['GET'])
def prod_update(request,code=None):
    d_date = 1
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    sections = Section.objects.filter(cooperative_id=cooperative)
    instance = get_object_or_404(Producteur, code=code)
    form = EditProdForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
		"instance": instance,
		"form":form,
        "d_date": d_date,
        "sections":sections
	}
    
    templateStr = render_to_string("cooperatives/prod_edt.html", context)
    return JsonResponse({'templateStr':templateStr,'id':code},safe=False)

@api_view(['POST'])
def edit_productor(request):
    id = request.POST['instance_id']
    instance = get_object_or_404(Producteur, id=id)
    form = EditProdForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            producteur = form.save(commit=False)
            producteur.save()
            return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
        else:
            return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)
        


@api_view(['GET'])
def edit_formatoin(request,id=None):
    d_date = 1
    instance = get_object_or_404(Formation, id=id)
    form = FormationForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
		"instance": instance,
		"form":form,
        "d_date": d_date
	}
    
    templateStr = render_to_string("cooperatives/edit_formation.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)

@api_view(['POST'])
def update_formation(request):
    id = request.POST['instance_id']
    instance = get_object_or_404(Formation, id=id)
    form = FormationForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            formation = form.save(commit=False)
            formation.save()
            form.save_m2m()
            return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
        else:
            return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)


@api_view(['GET'])
def edit_parcelle(request, id=None):
    d_date = 1
    instance = get_object_or_404(Parcelle, id=id)
    form = EditParcelleForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
		"instance": instance,
		"form":form,
        "d_date": d_date
	}
    
    templateStr = render_to_string("cooperatives/parcelle_edit.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)



@api_view(['POST'])
def parcelle_update(request):
    id = request.POST['instance_id']
    instance = get_object_or_404(Parcelle, id=id)
    form = EditParcelleForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            parcelle = form.save(commit=False)
            parcelle.save()
            return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
        else:
            return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)



#def update_section(request, id=None):
#    cooperative = Cooperative.objects.get(user_id=request.user.id)
#    instance = get_object_or_404(Section, id=id)
#    form = SectionForm(request.POST or None, request.FILES or None, instance=instance)
#    if form.is_valid():
#        instance = form.save(commit=False)
#        instance.cooperative_id = cooperative.id
#        instance.save()
#        messages.success(request, "Section Modifié Avec Succès", extra_tags='html_safe')
#        return HttpResponseRedirect(reverse('cooperatives:section'))
#    context = {
#        'instance' : instance,
#        'form' : form,
#    }
#    return render(request, "cooperatives/section_edit.html", context)



@api_view(['GET'])
def edit_section(request, id=None):
    d_date = 1
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Section, id=id)
    form = SectionForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
		"instance": instance,
		"form":form,
        "d_date": d_date
	}
    
    templateStr = render_to_string("cooperatives/section_edit.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)

@api_view(['POST'])
def update_section(request):
    id = request.POST['instance_id']
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Section, id=id)
    form = SectionForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.cooperative_id = cooperative.id
        instance.save()
        return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
    else:
        return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)



def delete_section(request,id=None):
    section = get_object_or_404(Section, id=id)
    section.delete()


@api_view(['GET'])
def edit_sous_section(request, id=None):
    d_date = 1
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    sections = Section.objects.all().filter(cooperative_id=cooperative)
    instance = get_object_or_404(Sous_Section, id=id)
    form = Edit_Sous_SectionForm(request.POST or None, request.FILES or None, instance=instance)
    
    context = {
        'instance' : instance,
        'form' : form,
        "sections":sections
    }
    templateStr = render_to_string("cooperatives/sous_section_edit.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)


@api_view(['POST'])
def update_sous_section(request):
    id = request.POST['instance_id']
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Sous_Section, id=id)
    form = Edit_Sous_SectionForm(request.POST or None, request.FILES or None, instance=instance)
    #form = SectionForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        s_section = form.save(commit=False)
        s_section.save()
        return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
    else:
        return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)



def delete_sous_section(request,id=None):
    item = get_object_or_404(Sous_Section, id=id)
    item.delete()


def monitoringSave(request):
    #print(request.POST['planting'])    
       espece = request.POST.getlist('espece')
       detailplanting = request.POST.getlist('d_planting')
       mort = request.POST.getlist('mort')
       #mature = request.POST.getlist('mature')
       recus = request.POST.getlist('recus')
       #print(detailplanting)

       #tot_mature = 0
       tot_mort = 0
       tot_recus = 0

       for mt,rcu in zip(mort,recus):           
           if mt != ''  and rcu != '':
                tot_recus = tot_recus + int(rcu)
                tot_mort = tot_mort + int(mt)  
                if int(mt) > int(rcu) : 
                    return JsonResponse({"msg": "Attention ! Plants mort d'une espece supperieur au plants recu","status":400},safe=False)
                    sys.exit(0)
                elif int(mt) < 0:
                    return JsonResponse({"msg": "Attention ! Nombres plants ne doit pas etre inferieur à 0","status":400},safe=False)
                    sys.exit(0)
           else:
               return JsonResponse({"msg": "Attention ! Verifier les champs renseignés","status":400},safe=False)
               sys.exit(0)
               
               
        
       if tot_recus <  tot_mort  : 
            return JsonResponse({"msg": "Attention! Total Plants mort supperieur au plants reçu","status":400},safe=False)
       else :
            monitoringForm = MonitoringForm(request.POST, request.FILES)
            if monitoringForm.is_valid():
               monitoring = monitoringForm.save(commit=False)
               monitoring.planting_id = request.POST['planting']
               monitoring.save()
               monitoringForm.save_m2m()


         
               detailmonitoring = DetailMonitoring()
               detailmonitoring.monitoring_id = monitoring.id
               detailmonitoring.save()      

               if request.POST['remplacer'] !='0': 

                   for es,de,mt in zip(espece,detailplanting,mort):
                        MonitoringEspece.objects.create(espece_id = int(es),detailplantingremplacement_id = int(de),mort=int(mt),  detailmonitoring_id = detailmonitoring.id)
               else :                

                    for es,de,mt in zip(espece,detailplanting,mort):
                        MonitoringEspece.objects.create(espece_id = int(es),detailplanting_id = int(de),mort=int(mt),  detailmonitoring_id = detailmonitoring.id)
              

               monitoring.mature_global = tot_recus - tot_mort
               monitoring.mort_global = tot_mort
               monitoring.save()               
           
           
               return JsonResponse({"msg": "Monitoring effectué avec succes !","status":200},safe=False)        
            else:
               return JsonResponse({"errors":monitoringForm.errors,"danger": "Enregistrement incorrect"},safe=False)

        

def espece_monitoring_view(request,id=None):
    monitoring = get_object_or_404(Monitoring, id=id)
    detail_monitoring = get_object_or_404(DetailMonitoring, monitoring_id=id)
    especemonitoring = MonitoringEspece.objects.filter(detailmonitoring_id = detail_monitoring.id)
    #print(especemonitoring)
    context = {
        'especemonitorings' : especemonitoring,
        'monitoring' : monitoring
    }
    
    templateStr = render_to_string("cooperatives/monitoring/especemonitoring.html", context)
    return JsonResponse({'templateStr':templateStr},safe=False)


def plantingSave(request):
    espece = request.POST.getlist('espece')
    nb_plante = request.POST.getlist('nb_plante')
    nb_plant_exitant  = request.POST['nb_plant_exitant']
    code_parc  = request.POST['parcelle']

 
    if code_parc == "":
        return JsonResponse({"msg": "Veillez renseigner le code parcelle","status":400},safe=False)
        sys.exit(0)


    if len(Parcelle.objects.filter(code=code_parc)) == 0:
        return JsonResponse({"msg": "Cette parcelle n'existe pas","status":400},safe=False)
        sys.exit(0)



    tot_espece = 0

    for nb,es in zip(nb_plante,espece):
        if es == '' or nb == '':          
            return JsonResponse({"msg": "Attention ! Verifier les champs renseignés","status":400},safe=False)
            sys.exit(0)
        elif int(nb) <= 0 :             
            return JsonResponse({"msg": " Attention ! Nombres plants doivent être superieur à 0 ","status":400},safe=False)
            sys.exit(0)
        else:
            tot_espece = tot_espece + int(nb)



    plantingForm = PlantingForm(request.POST, request.FILES)
    parcelle = Parcelle.objects.get(code=code_parc)
    
    if plantingForm.is_valid():
        planting = plantingForm.save(commit=False)
        planting.parcelle_id = parcelle.id 

        planting.save()

        for es,nb in zip(espece,nb_plante):
            DetailPlanting.objects.create(espece_id = int(es),nb_plante = int(nb),  planting_id = planting.id)



        planting.plant_recus = tot_espece
        planting.plant_total = planting.plant_recus + int(nb_plant_exitant)
        planting.save()


        return JsonResponse({"msg": "Planting effectué avec succes !","status":200},safe=False)        
    else:
        return JsonResponse({"errors":plantingForm.errors,"danger": "Enregistrement incorrect"},safe=False)

        
              
def producteurSave(request):

    cooperative = Cooperative.objects.get(user_id=request.user.id)   
    prodForm = ProdForm(request.POST, request.FILES)
    #print(prodForm)
    if prodForm.is_valid():
        producteur = prodForm.save(commit=False)
        producteur.cooperative_id = cooperative.id            
        producteur = producteur.save()
            # print(producteur)
        return JsonResponse({"msg": "Enregistrement effectué avec succes !","status":200},safe=False)        
    else:
        return JsonResponse({"errors":prodForm.errors,"danger": "Enregistrement incorrect"},safe=False)



def parcelleSave(request):
    parcelleForm = ParcelleForm(request.POST, request.FILES)
    prod = request.POST['producteur']    

    if prod == "":
        return JsonResponse({"msg": "Veillez renseigner le code proprietaire","status":400},safe=False)
        sys.exit(0)

    
    if len(Producteur.objects.filter(code=prod)) == 0:
        return JsonResponse({"msg": "Ce code ne correspond pas a un proprietaire","status":400},safe=False)
        sys.exit(0)
    
            
    producteur = Producteur.objects.get(code=prod)  
    
    if Parcelle.objects.filter(producteur_id = producteur.id) and len(Parcelle.objects.filter(producteur_id = producteur.id)) >= producteur.nb_parcelle:
        return JsonResponse({"msg": "Vous ne pouvez plus enregistrer de parcelle pour ce producteur","status":400},safe=False)
        sys.exit(0)
  
    if parcelleForm.is_valid():
        parcelle = parcelleForm.save(commit=False) 
        parcelle.producteur_id = producteur.id     
        if len(Parcelle.objects.filter(producteur_id = producteur.id)) >= 0 :
            tot ='P0'+str(len(Parcelle.objects.filter(producteur_id = producteur.id)) + 1)
            parcelle.code = "%s%s" % (producteur.code, tot)

        parcelle = parcelle.save()
        return JsonResponse({"msg": "Enregistrement effectué avec succes !","status":200},safe=False)        
    else:
        return JsonResponse({"errors":parcelleForm.errors,"danger": "Enregistrement incorrect"},safe=False)



############################formations 1000#################################################################
@login_required(login_url='connexion')
def tranning(request,id=None):
    activate = "formations"
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    producteurs = Producteur.objects.filter(cooperative_id=cooperative)
    campagnes = Campagne.objects.all()
    participants = Participantcoop.objects.filter(cooperative_id = cooperative)
    intitule = Intitule_Formation.objects.get(id=id)

    
    
    formationForm = FormationForm()
    participantForm = ParticipantcoopForm()

    

    context = {
        "producteurs":producteurs,
        "campagnes":campagnes,
        "formationForm":formationForm,
        "participantForm":participantForm,
        "activate": activate,
        "participants": participants,
        "intitule":intitule
    }

    return render(request, 'cooperatives/formations/insert.html', context)


def saveParticipant(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)

    participantForm = ParticipantcoopForm(request.POST or None, request.FILES or None)
    nom = request.POST['nom']
    #print(nom)
    if participantForm.is_valid():       
        participant = participantForm.save(commit=False)
        participant.cooperative_id = cooperative.id     
        participant.nom = nom       
        participant = participant.save()
        return JsonResponse({"msg": "Enregistrement effectué avec succes !","status":200},safe=False) 
    else:
        return JsonResponse({"errors":participantForm.errors,"danger": "Enregistrement incorrect"},safe=False)       



def deletes(request):
    d = request.POST['d'] 
    run = QueryDict(d,mutable=True)
    print(run.dict())
    #for i in d : 
    #    if i != '':
    #        print(i)
            #item = get_object_or_404(Participantcoop, id=int(i))
            #item.delete()
    
    
    
      
def participant_delete(request,id=None):
    item = get_object_or_404(Participantcoop, id=id)
    item.delete()


def formationSave(request):

    cooperative = Cooperative.objects.get(user_id=request.user.id) 

    nom = request.POST.getlist('nom')
    contact = request.POST.getlist('contact')
    #localite = request.POST.getlist('localite')
    parts = request.POST.getlist('participant')

    #print(nom,contact,localite,parts)

    formationForm = FormationForm(request.POST or None, request.FILES or None)
    if formationForm.is_valid():
       formation = formationForm.save(commit=False)
       formation.cooperative_id = cooperative.id  
       formation.save()
       formationForm.save_m2m()


       participants = Participantformation.objects.filter(formation_id = formation.id)
       #print(participants)

       for n,cnt,participant in zip(nom,contact,participants):           
            participant.nom = n
            participant.contact = cnt
            participant.save()


       for p in parts:
            del_participantscoop = Participantcoop.objects.filter(id = int(p))
            del_participantscoop.delete()


       return JsonResponse({"msg": "Formation enregistrer avec succes !","id":request.POST['intitule'],"status":200},safe=False)        
    else:
        return JsonResponse({"errors":formationForm.errors,"danger": "Enregistrement incorrect"},safe=False)




@login_required(login_url='connexion')
def export_formation_to_pdf(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    formation = get_object_or_404(Formation, id=id)
    nb_participant = Participantformation.objects.filter(formation_id = formation.id).count()
    participants = Participantformation.objects.filter(formation_id = id)
    producteurs = Producteur.objects.filter(cooperative_id=cooperative)
    #details = Detail_Formation.objects.filter(formation_id=instance)
    template_path = 'cooperatives/formations/pdf/formation_pdf.html'
    context = {
        'cooperative':cooperative, 
        'formation':formation,
        'participants':participants,
        'nb_participant':nb_participant,
        "producteurs":producteurs
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Formation.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy viewp
    if pisa_status.err:
        return HttpResponse('Une Erreure est Survenue, Réessayer SVP...' + html + '</pre>')
    return response


def changeSection(request):

    id = request.POST['id'] 

    templateStr = '  <option selected value="">-- Select --</option> '

    if id != '': 
        s_section = Sous_Section.objects.filter(section_id = id)        
        for sect in s_section :
            templateStr =  ' <option value="'+str(sect.id)+'">'+ sect.libelle +'  </option>'


    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)



@api_view(['POST'])
def contactProd(request):
    nom = request.POST['nom']

    producteur = Producteur.objects.get(nom__exact = nom)
   #print(producteur.contacts)
    if producteur:
        return JsonResponse({'contact':producteur.contacts},safe=False)
    else:
        pass


############################remplacement 1000#################################################################
def remplacement_monitoring_view(request,id):
    monitoring = get_object_or_404(Monitoring, id=id)
    detail_monitoring = get_object_or_404(DetailMonitoring, monitoring_id=id)
    especemonitoring = MonitoringEspece.objects.filter(detailmonitoring_id = detail_monitoring.id)
    especes_plants = Espece.objects.all()
    formRemplacement = RemplacementMonitoringForm()
    #print(especemonitoring)
    context = {
        'especes' : especemonitoring,
        'monitoringremplaces' : monitoring,
        'especes_plants': especes_plants,
        'formRemplacement':formRemplacement
    }
    templateStr = render_to_string("cooperatives/monitoring/monitoringremplace.html", context)
    return JsonResponse({'templateStr':templateStr},safe=False)



def RemplaceSave(request):

    espece = request.POST.getlist('espece')
    mort = request.POST.getlist('mort')
    remplacer = request.POST.getlist('remplacer')
    recus = request.POST.getlist('recus')
    newrecus = request.POST.getlist('newrecus')
    newespece = request.POST.getlist('newespece')
    mortn = request.POST.getlist('mortn')
    remplacern = request.POST.getlist('remplacern')
    #print(espece,mort,remplacer,recus,newrecus,newespece,mortn,remplacern)

    tot_mort = 0
    tot_remplacer = 0
    tot_recus = 0
    tot_new = 0
    tot_mortn = 0
    tot_remplacern = 0

    for es,m,rp,rc in zip(espece,mort,remplacer,recus):
        if rc == '0':
            m =0
        
        if rp != '' :
            tot_mort = tot_mort + int(m)
            tot_remplacer = tot_remplacer + int(rp)
            tot_recus = tot_recus + int(rc)
            if int(rp) > int(m) : 
                    return JsonResponse({"msg": "Attention ! Plants de remplacement d'une espèce supperieur au plants morts","status":400},safe=False)
                    sys.exit(0)
            elif int(rp)< 0:
                return JsonResponse({"msg": "Attention ! Nombres plants ne doit pas être inférieur à 0","status":400},safe=False)
                sys.exit(0)
        else:
            return JsonResponse({"msg": "Attention ! Verifier les champs renseignés","status":400},safe=False)
            sys.exit(0)

    monitoring = get_object_or_404(Monitoring, id=int(request.POST['monitoring']))
    planting = get_object_or_404(Planting, id=monitoring.planting.id)

    date = request.POST['date']

    remplacementM = RemplacementMonitoring()
    remplacementM.date = date
    remplacementM.monitoring_id = monitoring.id
    remplacementM.save()



    for es,m,rp,rc in zip(espece,mort,remplacer,recus):       
        DetailPlantingRemplacement.objects.create(espece_id = int(es),nb_plante = int(rc),planting_id = planting.id,remplacer_id = remplacementM.id)
            


    for  mtn,rpn,nw,nes in zip(mortn,remplacern,newrecus,newespece):
        tot_mortn = tot_mortn + int(mtn)
        tot_remplacern = tot_remplacern + int(rpn)
        tot_new = tot_new + int(nw)
        if nes == "" and nw:
            pass
        elif nes != "" and nw :
            DetailPlantingRemplacement.objects.create(espece_id = int(nes),nb_plante = int(nw),planting_id = planting.id,remplacer_id = remplacementM.id)
        


    planting.plant_recus = tot_recus + tot_new
    planting.save()            

        #print(planting.plant_recus)
       

    for es,m,rp,rc in zip(espece,mort,remplacer,recus):
        if rc == '0':
            m = 0

        MonitoringEspeceremplacement.objects.create(espece_id = int(es),remplacer = int(rp),mort=int(m),futur = int(m)-int(rp), recu = int(rc),remplacement_id= remplacementM.id)



    for nes,nrc in zip(newespece,newrecus):
        if nes == "" and nrc:
            pass
        elif nes != "" and nrc :
            MonitoringEspeceremplacement.objects.create(espece_id = int(nes),remplacer = 0,mort=0,futur=0,  recu = int(nrc),remplacement_id= remplacementM.id)


      

    monitoring.mort_global = tot_mort - tot_remplacer   
    monitoring.mature_global =  monitoring.mature_global + tot_remplacer
    monitoring.save()  


    return JsonResponse({"msg": "Remplacement effectué avec succes!","status":300},safe=False)

    

@api_view(['POST'])
def endremplaceSave(request):
    data = request.POST['data']
    run = QueryDict(data,mutable=True)
     #runs = list(run.items())
    espece = run.pop('espece')
    mort = run.pop('mort') 
    remplacer = run.pop('remplacer')  
    recus = run.pop('recus') 
    newrecus = run.pop('newrecus') 
    newespece = run.pop('newespece') 
    mortn = run.pop('mortn') 
    remplacern =run.pop('remplacern') 

    tot_mort = 0
    tot_remplacer = 0
    tot_recus = 0
    tot_new = 0
    tot_mortn = 0
    tot_remplacern = 0


    for es,m,rp,rc in zip(espece,mort,remplacer,recus):
        if rc == '0':
            m =0
        
        if rp != '' :
            tot_mort = tot_mort + int(m)
            tot_remplacer = tot_remplacer + int(rp)
            tot_recus = tot_recus + int(rc)
            if int(rp) > int(m) : 
                    return JsonResponse({"msg": "Attention ! Plants de remplacement d'une espèce supperieur au plants morts","status":400},safe=False)
                    sys.exit(0)
            elif int(rp)< 0:
                return JsonResponse({"msg": "Attention ! Nombres plants ne doit pas être inférieur à 0","status":400},safe=False)
                sys.exit(0)
        else:
            return JsonResponse({"msg": "Attention ! Verifier les champs renseignés","status":400},safe=False)
            sys.exit(0)


    for moni in run.pop('monitoring'):
         monitoring = get_object_or_404(Monitoring, id=int(moni))
    
    for d in run.pop('date'):
         date = d

    planting = get_object_or_404(Planting, id=monitoring.planting.id)

    remplacementM = RemplacementMonitoring()
    remplacementM.date = date
    remplacementM.monitoring_id = monitoring.id
    remplacementM.save()
    


    for es,m,rp,rc in zip(espece,mort,remplacer,recus):
        DetailPlantingRemplacement.objects.create(espece_id = int(es),nb_plante = int(rc),planting_id = planting.id,remplacer_id = remplacementM.id)
            


    for  mtn,rpn,nw,nes in zip(mortn,remplacern,newrecus,newespece):
        tot_mortn = tot_mortn + int(mtn)
        tot_remplacern = tot_remplacern + int(rpn)
        tot_new = tot_new + int(nw)
        if nes == "" and nw:
            pass
        elif nes != "" and nw :
            DetailPlantingRemplacement.objects.create(espece_id = int(nes),nb_plante = int(nw),planting_id = planting.id,remplacer_id = remplacementM.id)

    
    planting.plant_recus = tot_recus + tot_new
    planting.save()

    
    #print(planting)    
    #print(run.pop('monitoring'),run.pop('mort'))

    

    for m,es,rc,rp in zip(mort,espece,recus,remplacer):
        if rc == '0':
            m = 0

        MonitoringEspeceremplacement.objects.create(espece_id = int(es),remplacer = int(rp),mort=int(m),futur = int(m)-int(rp), recu = int(rc),remplacement_id= remplacementM.id)


    for nes,nrc in zip(newespece,newrecus):
        if nes == "" and nrc:
            pass
        elif nes != "" and nrc :
            MonitoringEspeceremplacement.objects.create(espece_id = int(nes),remplacer = 0,mort=0,futur=0,recu = int(nrc),remplacement_id= remplacementM.id)

    
  

    monitoring.mort_global = tot_mort - tot_remplacer   
    monitoring.mature_global =  monitoring.mature_global + tot_remplacer
    monitoring.save()   




 
def esrempla_monitoring_view(request,id=None):
    remplace = RemplacementMonitoring.objects.get(id=id)
    especemonitoring = MonitoringEspeceremplacement.objects.filter(remplacement_id = id)
    #print(especemonitoring)
    context = {
        'especemonitorings' : especemonitoring,
        'remplace' : remplace
    }
    templateStr = render_to_string("cooperatives/monitoring/esremplacer.html", context)
    return JsonResponse({'templateStr':templateStr},safe=False)




def rempend_monitoring_view(request,id=None):
    remplace = RemplacementMonitoring.objects.get(id=id)
    especemonitoring = MonitoringEspeceremplacement.objects.filter(remplacement_id = id)
    especes_plants = Espece.objects.all()
    formRemplacement = RemplacementMonitoringForm()
    #print(especemonitoring)
    context = {
        'especes' : especemonitoring,
        'especes_plants': especes_plants,
        'formRemplacement':formRemplacement,
        'remplace':remplace
    }
    templateStr = render_to_string("cooperatives/monitoring/aftermoni_espece.html", context)
    return JsonResponse({'templateStr':templateStr},safe=False)


def monitoring_form_view(request,id=None):
    

    try:
        monitoring = Monitoring.objects.filter(planting_id = id).latest('id')
        #remplacer = RemplacementMonitoring.objects.filter(monitoring_id = monitoring.id).latest('id')
        rmp = len(RemplacementMonitoring.objects.filter(monitoring_id= monitoring.id))
        if rmp > 0 :
            instance = get_object_or_404(Planting, id=id)
            remplacer = RemplacementMonitoring.objects.filter(monitoring_id = monitoring.id).latest('id')
            remplmonitoringViews = DetailPlantingRemplacement.objects.filter(planting_id=instance.id , remplacer_id=remplacer.id )
            monitoringForm = MonitoringForm()
            context = {
            "remplacer":remplacer,
            'instance' : instance,
            'monitoringForm' : monitoringForm,
            "remplmonitoringViews" : remplmonitoringViews
            }
            templateStr = render_to_string("cooperatives/monitoring/form_monitoringrplace.html", context)
            return JsonResponse({'templateStr':templateStr,'id':id},safe=False)
        elif rmp == 0 :
            monitorings = Monitoring.objects.filter(planting_id = id).order_by('-id')
            
            for moni in monitorings :
                idn = moni.id - 1
                if len(RemplacementMonitoring.objects.filter(monitoring_id= idn)) > 0:
                    inst = get_object_or_404(Planting, id=id)
                    rempla = RemplacementMonitoring.objects.filter(monitoring_id = idn).latest('id')
                    remplmonitoringViews = DetailPlantingRemplacement.objects.filter(planting_id=inst.id , remplacer_id=rempla.id )
                    monitoringForm = MonitoringForm()
                    context = {
                    "remplacer":rempla,
                    'instance' : inst,
                    'monitoringForm' : monitoringForm,
                    "remplmonitoringViews" : remplmonitoringViews
                    }
                    templateStr = render_to_string("cooperatives/monitoring/form_monitoringrplace.html", context)
                    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)
                    sys.exit(0)


    except Monitoring.DoesNotExist :
        instance = get_object_or_404(Planting, id=id)
        remplmonitoringViews = DetailPlanting.objects.filter(planting_id=instance)
        monitoringForm = MonitoringForm()
        context = {
        'instance' : instance,
        'monitoringForm' : monitoringForm,
        "remplmonitoringViews" : remplmonitoringViews
        }
        templateStr = render_to_string("cooperatives/monitoring/form_monitoring.html", context)
        return JsonResponse({'templateStr':templateStr,'id':id},safe=False)


##plus pris en compte#####
def deleteEspece(request, id=None):
    item = get_object_or_404(MonitoringEspece, id=id)
    item.delete()

    return JsonResponse({'id':id},safe=False) 


############################remplacement 1000#################################################################

@login_required(login_url='connexion')
def production(request):
    activate = "productions"
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    productions = Production.objects.filter(parcelle__producteur__cooperative_id=cooperative).order_by('annee')
    #campagnes = CampagneProduction.objects.filter(annee = datetime.datetime.now().year)
    form = ProductionForm()
    if request.method == 'POST':
        form = ProductionForm(request.POST, request.FILES)
        if form.is_valid():
            production = ProductionForm.save(commit=False)
            for parcelle in parcelles.iterator():
                production.parcelle_id = parcelle.id
                production.save()
                # print(production)
        messages.success(request, "Production Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:productions'))
    context = {
        "cooperative":cooperative,
        "parcelles": parcelles,
        "productions": productions,
        #'campagnes':campagnes,
        'form': form,
    }
    return render(request, "cooperatives/productions/productions.html", context)


def productionSave(request):
    parc = request.POST['parcelles']
    qty = request.POST['qteProduct']
    form = ProductionForm(request.POST, request.FILES)

    if parc == "":
        return JsonResponse({"msg": "Veillez renseigner le code parcelle","status":400},safe=False)
        sys.exit(0)


    if len(Parcelle.objects.filter(code=parc)) == 0:
        return JsonResponse({"msg": "Ce code ne correspond pas a une parcelle ","status":400},safe=False)
        sys.exit(0)

    
    parcelle = Parcelle.objects.get(code=parc)
    maxkgv1 = parcelle.superficie * 800

    if len(Production.objects.filter(parcelle = parcelle.id)) == 0 :   
         if int(qty) > int(maxkgv1):
            return JsonResponse({"msg": "La capacitée de production en kg de cette parcelle est atteinte ","status":400},safe=False)
            sys.exit(0)
    elif len(Production.objects.filter(parcelle = parcelle.id)) == 1 :
        production = Production.objects.get(parcelle = parcelle.id)
        sommeKg = 0
        sommeKg = production.qteProduct + int(qty)

        if sommeKg > int(maxkgv1):
            return JsonResponse({"msg": "La capacitée de production en kilogramme ("+str(round(maxkgv1,1))+"kg)  de cette parcelle est atteinte" ,"status":400},safe=False)
            sys.exit(0)
    
    elif len(Production.objects.filter(parcelle = parcelle.id)) > 1 :
        productions1 = Production.objects.filter(parcelle = parcelle)
        sommeKg = 0

        for prod in productions1 : 
            sommeKg = sommeKg + prod.qteProduct


        if sommeKg > int(maxkgv1):
            return JsonResponse({"msg": "La capacitée de production en kilogramme ("+str(round(maxkgv1,1))+"kg)  de cette parcelle est atteinte" ,"status":400},safe=False)
            sys.exit(0)

    

    if form.is_valid():
        product = form.save(commit=False) 
        product.parcelle_id = parcelle.id   
        product = product.save()
        return JsonResponse({"msg": "Enregistrement effectué avec succes !","status":200},safe=False)        
    else:
        return JsonResponse({"errors":form.errors,"danger": "Enregistrement incorrect"},safe=False)
    
   

    #print(sommeKg)



@api_view(['GET'])
def edit_product(request, id=None):
    instance = get_object_or_404(Production, id=id)
    form = EditProductionForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
		"instance": instance,
		"form":form,
	}
    
    templateStr = render_to_string("cooperatives/productions/product_edit.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)



@api_view(['POST'])
def production_update(request):
    id = request.POST['instance_id']
    qty = request.POST['qteProduct']
    parcelle_id = request.POST['parcelle']
    instance = get_object_or_404(Production, id=id)
    form = EditProductionForm(request.POST or None, request.FILES or None, instance=instance)

    parcelle = Parcelle.objects.get(id=parcelle_id)
    maxkgv1 = parcelle.superficie * 800

    if len(Production.objects.filter(parcelle = parcelle.id)) == 0 :   
         if int(qty) > int(maxkgv1):
            return JsonResponse({"msg": "La capacitée de production en kg de cette parcelle est atteinte ","status":400},safe=False)
            sys.exit(0)
    elif len(Production.objects.filter(parcelle = parcelle.id)) == 1 :
        production = Production.objects.get(parcelle = parcelle.id)
        sommeKg = 0
        sommeKg = production.qteProduct + int(qty)

        if sommeKg > int(maxkgv1):
            return JsonResponse({"msg": "La capacitée de production en kilogramme ("+str(round(maxkgv1,1))+"kg)  de cette parcelle est atteinte" ,"status":400},safe=False)
            sys.exit(0)
    
    elif len(Production.objects.filter(parcelle = parcelle.id)) > 1 :
        productions1 = Production.objects.filter(parcelle = parcelle)
        sommeKg = 0

        for prod in productions1 : 
            sommeKg = sommeKg + prod.qteProduct


        if sommeKg > int(maxkgv1):
            return JsonResponse({"msg": "La capacitée de production en kilogramme ("+str(round(maxkgv1,1))+"kg)  de cette parcelle est atteinte" ,"status":400},safe=False)
            sys.exit(0)


    if request.method == 'POST':
        if form.is_valid():
            parcelle = form.save(commit=False)
            parcelle.save()
            return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
        else:
            return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)

    
    


def production_delete(request,id=None):
    production = get_object_or_404(Production, id=id)
    production.delete()

    