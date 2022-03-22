from collections import Counter
import csv
import datetime
from itertools import product
import os
from cv2 import findEssentialMat
from django.forms.fields import DateField
from django.forms.forms import Form
from django.template.loader import render_to_string
from django.template.context import Context

import folium
import pandas as pd
from django.core import serializers
import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader, RequestContext
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from django_pandas.io import read_frame
from folium import plugins, raster_layers
from folium.plugins import MarkerCluster
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from xhtml2pdf import pisa

from rest_framework.response import Response
from rest_framework.decorators import api_view

from traceability import settings

from .serializers import ParcelleSerializer, PepiniereSerializer, PlantingSerializer, DetailsPlantingSerializer, \
    SectionSerializer, ProducteurSerializer, ParcelleMobileSerializer, ProductionSerializer, CooperativeSerializer, \
    DetailsPlantingMobileSerializer
from cooperatives.models import Participantformation, Planting, DetailPlanting, Production
from django.db.models import Count
from django.template.loader import get_template, render_to_string


class PlantingParifApiView(ListAPIView):
    queryset = Planting.objects.all()
    p_count = queryset.count()
    serializer_class = PlantingSerializer
#
#
# class DetailPlantingParifApiView(ListAPIView):
#     queryset = DetailPlanting.objects.all()
#     p_count = queryset.count()
#     print(p_count)
#     serializer_class = DetailsPlantingSerializer


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = findEssentialMat.find(uri)
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


@api_view(['GET'])
def map_parcelles(request):
    parcelles = Parcelle.objects.all().order_by('code')
    serializer = ParcelleSerializer(parcelles, many=True)
    nb_parcelles = parcelles.count()
    print(nb_parcelles)
    return Response(serializer.data)


@api_view(['GET'])
def map_cooperative(request):
    id = request.GET.get('id')

    if id != "":
        cooperative = get_object_or_404(Cooperative, id=id)
        parcelle_coops = Parcelle.objects.filter(producteur__cooperative_id=cooperative)
        nb_parcelles = parcelle_coops
        section_coops = Section.objects.filter(cooperative_id=cooperative)

        sections = serializers.serialize('json', section_coops)

        context = {
            "cooperative": cooperative,
            "parcelle_coops": parcelle_coops,
            "nb_parcelles": nb_parcelles,
        }

        templateStr = render_to_string("cooperatives/carte_coop.html", context)
        return JsonResponse({'templateStr': templateStr, 'id': id, 'sections': sections}, safe=False)

    else:
        cooperatives = Cooperative.objects.all()
        context = {
            'cooperatives': cooperatives
        }
        templateStr = render_to_string("cooperatives/carte_coop.html", context)
        return JsonResponse({'templateStr': templateStr, 'id': ""}, safe=False)


@api_view(['GET'])
def map_section(request):
    id = request.GET.get('id')
    id_coop = request.GET.get('id_coop')

    if id != "" and id_coop != "":
        section_coop = Section.objects.filter(id=id)

        context = {
            "section_coop": section_coop,
        }
        templateStr = render_to_string("cooperatives/carte_section.html", context)
        return JsonResponse({'templateStr': templateStr, 'id': id, 'id_coop': id_coop}, safe=False)

    elif id == "" and id_coop != "":
        cooperative = get_object_or_404(Cooperative, id=id_coop)
        parcelle_coops = Parcelle.objects.filter(producteur__cooperative_id=cooperative)
        nb_parcelles = parcelle_coops

        context = {
            "cooperative": cooperative,
            "parcelle_coops": parcelle_coops,
            "nb_parcelles": nb_parcelles,
        }

        templateStr = render_to_string("cooperatives/carte_coop.html", context)
        return JsonResponse({'templateStr': templateStr, 'id': id, 'id_coop': id_coop}, safe=False)


@api_view(['GET'])
def api_detail_cooperative(request, id):
    cooperative = get_object_or_404(Cooperative, id=id)
    queryset = Planting.objects.filter(producteur__cooperative_id=id)
    p_count = queryset.count()
    serializer = PlantingSerializer(queryset, many=True)

    print(p_count)
    return Response(serializer.data)


@api_view(['GET'])
def map_plantings_espece_old(request, id):
    queryset = DetailPlanting.objects.filter(planting_id=id)
    p_count = queryset.count()
    print(p_count)

    data = serializers.serialize('json', queryset)

    return JsonResponse({'data': data}, safe=False)


from django.contrib.auth.models import Group


@login_required(login_url='connexion')
def catre_parcelles(request):
    cooperatives = Cooperative.objects.all()
    context = {
        'cooperatives': cooperatives
    }
    return render(request, 'carte.html', context)


@api_view(['GET'])
def coop_parcelles(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    parcelle_coop = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    serializer = PlantingSerializer(parcelle_coop, many=True)
    nb_parcelles = parcelle_coop.count()
    print(nb_parcelles)
    return Response(serializer.data)


@api_view(['GET'])
def section_parcelles(request, id=None):
    section = get_object_or_404(Section, id=id)
    parcelle_coop = Planting.objects.filter(parcelle__producteur__section_id=section)
    serializer = PlantingSerializer(parcelle_coop, many=True)
    nb_parcelles = parcelle_coop.count()
    print(nb_parcelles)
    return Response(serializer.data)


@api_view(['GET'])
def coop_section(request, id_coop=None):
    cooperative = get_object_or_404(Cooperative, id=id_coop)
    section_coop = Section.objects.filter(cooperative_id=cooperative)
    serializer = SectionSerializer(section_coop, many=True)
    nb_sections = section_coop.count()
    print(nb_sections)
    return Response(serializer.data)


# @api_view(['GET'])
# def Planting_map(request):
#     # cooperative = get_object_or_404(Cooperative, id=id)
#     plantings = Planting.objects.all()
#     serializer = DetailPlantingSerializer(plantings, many=True)
#     nb_plantings = plantings.count()
#     print(nb_plantings)
#     return Response(serializer.data)

@login_required(login_url='connexion')
def catre_parcelles_coop(request):
    return render(request, 'carte_coop.html')


from .forms import LoginForm, PepiniereForm, SemenceForm, ProjetForm, PrimeForm
from .models import (
    Cooperative,
    Espece,
    Pepiniere,
    Semence_Pepiniere,
    Sous_Prefecture,
    Origine,
    Prime,
    Projet,
    # Pepiniere,
    Activite,
    Region,
    # Campagne, Detail_Pepiniere, Detail_Retrait,
    # Formations,
)

from cooperatives.models import (
    Producteur,
    Parcelle,
    Planting,
    # Details_planting,
    Section,
    Sous_Section, Formation, Detail_Formation, DetailPlanting,
    Monitoring,
)


def connexion(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            # utilisateur valide et actif(is_active=True)
            # "request.user == user"
            dj_login(request, user)
            group = request.user.groups.filter(user=request.user)[0]
            if group.name == "COOPERATIVES":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('cooperatives:dashboard'))
            elif group.name == "ADMIN":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('accueil'))
            elif group.name == "CLIENTS":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('clients:dashboard'))
            elif group.name == "AGROFORESTERIE":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('parif:dashboard'))
            elif group.name == "REFORESTATION":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('parif:dashboard'))
            else:
                messages.error(request, "Désolé vous n'estes pas encore enregistrer dans notre Sytème")
                return HttpResponseRedirect(reverse('connexion'))
        else:
            request.session['invalid_user'] = 1  # 1 == True
            messages.error(request, "Echec de Connexion, Assurez-vous d'avoir entrer le bon login et le bon Mot de Passe SVP !")
            return HttpResponseRedirect(reverse('connexion'))
    return render(request, 'parametres/login.html', {'login_form': login_form})


def loggout(request):
    logout(request)
    return HttpResponseRedirect(reverse('connexion'))


@login_required(login_url='connexion')
def index(request):
    activate = 'accueil'
    cooperatives = Cooperative.objects.all()
    parcelles = Parcelle.objects.all()
    producteurs = Producteur.objects.all()
    # communautes = Communaute.objects.all()
    # nb_communautes = Communaute.objects.all().count()
    nb_cooperatives = Cooperative.objects.all().count()
    nb_producteurs = Producteur.objects.all().count()
    nb_parcelles = Parcelle.objects.all().count()
    Superficie = Parcelle.objects.aggregate(total=Sum('superficie'))['total']
    Total_plant = Planting.objects.aggregate(total=Sum('plant_recus'))['total']
    production = Production.objects.aggregate(total=Sum('qteProduct'))['total']
    petite_production = Production.objects.filter(campagne="petite").aggregate(total=Sum('qteProduct'))['total']
    grande_production = Production.objects.filter(campagne="grande").aggregate(total=Sum('qteProduct'))['total']

    for coop in cooperatives:
        coop.parcelles = Parcelle.objects.filter(producteur__cooperative=coop).count()
        coop.productions = Production.objects.filter(parcelle__producteur__cooperative=coop).aggregate(total=Sum('qteProduct'))['total']
        coop.plants = Planting.objects.filter(parcelle__producteur__cooperative=coop).aggregate(total=Sum('plant_recus'))['total']
        coop.superficies = int(Parcelle.objects.filter(producteur__cooperative=coop).aggregate(total=Sum('superficie'))[ 'total'])
        coop.Superf = Parcelle.objects.filter(producteur__cooperative=coop).aggregate(total=Sum('superficie'))[ 'total']

    context = {
        'cooperatives': cooperatives,
        'nb_cooperatives': nb_cooperatives,
        'nb_producteurs': nb_producteurs,
        'nb_parcelles': nb_parcelles,
        'Superficie': Superficie,
        'Total_plant': Total_plant,
        'producteurs': producteurs,
        'production': production,
        'petite_production': petite_production,
        'grande_production': grande_production,
        'activate':activate
    }
    return render(request, 'parametres/index.html', context)


@login_required(login_url='connexion')
def detail_coop(request, id=None):
    activate = "dashboard"
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_nb_producteurs =
    section = Section.objects.filter(cooperative_id=cooperative)
    sous_sections = Sous_Section.objects.filter(section__cooperative_id=cooperative)
    # section_prod = Producteur.objects.all().filter(section_id__in=section).count()
    section_prod = Section.objects.annotate(nb_producteur=Count('producteurs'))
    prod_section = Producteur.objects.filter(section_id__in=section).count()
    coop_nb_producteurs = Producteur.objects.filter(cooperative_id=cooperative).count()
    nb_formations = Formation.objects.filter(cooperative_id=cooperative).count()
    parcelles_section = Parcelle.objects.filter(producteur__section_id__in=section).count()
    # section_parcelle = Section.objects.annotate(nb_producteur=Count('producteurs.parcelles'))
    coop_nb_parcelles = Parcelle.objects.filter(producteur__section__cooperative_id=cooperative).count()
    coop_superficie = \
    Parcelle.objects.filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    section_superf = Parcelle.objects.filter(producteur__section_id__in=section).aggregate(total=Sum('superficie'))[
        'total']
    # section_plating = Planting.objects.filter(parcelle__producteur__section_id__in=section).aggregate(total=Sum('plant_recus'))['total']
    # plantings = DetailPlanting.objects.values("espece__libelle").filter(planting__parcelle__producteur__cooperative_id=cooperative).annotate(plante=Sum('plant_recus'))
    coop_plants_total = \
    DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).aggregate(
        total=Sum('nb_plante'))['total']
    context = {
        'cooperative': cooperative,
        'coop_nb_producteurs': coop_nb_producteurs,
        'coop_nb_parcelles': coop_nb_parcelles,
        'coop_superficie': coop_superficie,
        'nb_formations': nb_formations,
        'section': section,
        'sous_sections': sous_sections,
        'prod_section': prod_section,
        'section_prod': section_prod,
        # 'section_parcelle': section_parcelle,
        'parcelles_section': parcelles_section,
        'coop_plants_total': coop_plants_total,
        'section_superf': section_superf,
        'activate': activate
        # 'labels': labels,
        # 'data': data,
    }
    return render(request, 'Coop/cooperative.html', context)


def prod_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)  # .order_by("-update_le")
    # coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_producteurs': coop_producteurs,
    }
    return render(request, 'Coop/coop_producteurs.html', context)


def parcelle_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # sections = Section.objects.all().filter(cooperative_id=cooperative)
    coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_parcelles': coop_parcelles,

    }
    return render(request, 'Coop/coop_parcelle.html', context)


def formations(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_formations = Formation.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'formations': coop_formations,
    }
    return render(request, 'Coop/coop_formations.html', context)


def planting_coop(request, id=None, p_id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    sections = Section.objects.all().filter(cooperative_id=cooperative)
    # planting = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    plantings = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'plantings': plantings,
        'sections': sections,
    }
    return render(request, 'cooperatives/planting_coop_update.html', context)


# secteur pepiniere semences
@login_required(login_url='connexion')
def pepiniere(request):
    pepinieres = Pepiniere.objects.all()
    pepiForm = PepiniereForm()
    activate = "pepiniere"
    if request.method == 'POST':
        pepiForm = PepiniereForm(request.POST, request.FILES)
        if pepiForm.is_valid():
            pepiniere = pepiForm.save(commit=False)
            pepiniere = pepiniere.save()
            print(pepiniere)
        messages.success(request, "Site Pépinière Ajouté avec succès")
        # return HttpResponseRedirect(reverse('pepinieres'))

    context = {
        'pepinieres': pepinieres,
        'pepiForm': pepiForm,
        'activate': activate
    }
    return render(request, 'parametres/pepinieres.html', context)


def catre_pepiniere(request):
    pepinieres = Pepiniere.objects.all()
    context = {
        'pepinieres': pepinieres,
    }
    return render(request, 'parametres/carte_pepiniere.html', context)


@api_view(['GET'])
def map_pepinieres(request):
    pepinieres = Pepiniere.objects.all().order_by('id')
    serializer = PepiniereSerializer(pepinieres, many=True)
    nb_parcelles = pepinieres.count()
    print(nb_parcelles)
    return Response(serializer.data)


def Editpepiniere(request, id=None):
    instance = get_object_or_404(Pepiniere, id=id)
    pepiForm = PepiniereForm(request.POST or None, request.FILES or None, instance=instance)

    context = {
        "instance": instance,
        "pepiForm": pepiForm,
    }

    templateStr = render_to_string("cooperatives/edit_pepiniere.html", context)
    return JsonResponse({'templateStr': templateStr, 'id': id}, safe=False)


def update_pepiniere(request):
    id = request.POST['instance_id']
    instance = get_object_or_404(Pepiniere, id=id)
    pepiForm = PepiniereForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if pepiForm.is_valid():
            pepiniere = pepiForm.save(commit=False)
            pepiniere.save()
            return JsonResponse({"msg": "Modification effectuée avec success", "status": 200, "id": id}, safe=False)
        else:
            return JsonResponse({"errors": pepiForm.errors, "danger": "Modification incorrect"}, safe=False)


@login_required(login_url='connexion')
def detail_pepiniere(request, id=None):
    # cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Pepiniere, id=id)
    semences = Semence_Pepiniere.objects.all().filter(pepiniere_id=instance)
    total_plants_a_produire = \
    Semence_Pepiniere.objects.all().filter(pepiniere_id=instance).aggregate(total=Sum('production'))['total']

    semenceForm = SemenceForm()
    # print(semenceForm)

    if request.method == 'POST':
        semenceForm = SemenceForm(request.POST, request.FILES)
        if semenceForm.is_valid():
            semence_recu = semenceForm.save(commit=False)
            semence_recu.pepiniere_id = instance.id
            semence_recu = semence_recu.save()
            # semenceForm.save_m2m()

            messages.success(request, "Enregistrement effectué avec succès")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return HttpResponse("Enregistrement effectué avec succès")

    context = {
        'instance': instance,
        'semences': semences,
        'semenceForm': semenceForm,
        'total_plants_a_produire': total_plants_a_produire,
    }
    return render(request, 'cooperatives/detail_pepiniere.html', context)


@api_view(['POST'])
def edit_semence(request):
    id = request.POST['instance_id']
    instance = get_object_or_404(Semence_Pepiniere, id=id)
    form = SemenceForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            semence = form.save(commit=False)
            semence.save()
            return JsonResponse({"msg": "Modification effectuée avec success", "status": 200, "id": id}, safe=False)
        else:
            return JsonResponse({"errors": form.errors, "danger": "Modification incorrect"}, safe=False)


def edit_semence_view(request):
    id = request.GET['id']
    instance = get_object_or_404(Semence_Pepiniere, id=id)
    form = SemenceForm(request.POST or None, request.FILES or None, instance=instance)

    context = {
        "instance": instance,
        "semenceForm": form,
    }

    templateStr = render_to_string("cooperatives/edit_semence.html", context)
    return JsonResponse({'templateStr': templateStr, 'id': id}, safe=False)


def delete_semence(request, id=None):
    semence = get_object_or_404(Semence_Pepiniere, id=id)
    semence.delete()


@api_view(['GET'])
def semence_by_pepiniere(request, id=None):
    instance = get_object_or_404(Pepiniere, id=id)
    semences = Semence_Pepiniere.objects.all().filter(pepiniere_id=instance)
    total_plants_a_produire = \
    Semence_Pepiniere.objects.all().filter(pepiniere_id=instance).aggregate(total=Sum('production'))['total']

    context = {
        "semences": semences,
        "instance": instance,
        "t_semence": total_plants_a_produire
    }

    templateStr = render_to_string("cooperatives/tab_semences.html", context)
    return JsonResponse({'templateStr': templateStr, 'id': id}, safe=False)


@api_view(['GET'])
def show_monitoring(request, id=None):
    # cooperative = Cooperative.objects.get(user_id=request.user.id)
    monitorings = Monitoring.objects.filter(planting_id=id)
    planting = Planting.objects.get(id=id)
    eye = 1

    if not monitorings:
        return JsonResponse({'msg': "Aucun monitoring effectué sur cette parcelle !", "status": 400}, safe=False)
    else:
        context = {
            "monitorings": monitorings,
            # "cooperative": cooperative,
            "planting": planting
        }

    templateStr = render_to_string("parametres/tab_monitoring.html", context)
    return JsonResponse({'templateStr': templateStr, 'id': id}, safe=False)


@api_view(['GET'])
def map_plantings_espece(request, id=None):
    groups = []
    user = request.user
    if user.is_authenticated:
        groups = list(user.groups.values_list('name', flat=True))

    queryset = DetailPlanting.objects.filter(planting_id=id)
    planting = Planting.objects.get(id=id)

    t_planting = DetailPlanting.objects.filter(planting_id=planting).aggregate(total=Sum('nb_plante'))['total']
    p_count = queryset.count()

    if not queryset:
        return JsonResponse({'msg': "Desolé! Cette parcelle ne contient pas d'espece .", "status": 400}, safe=False)
    else:
        context = {
            't_planting': t_planting,
            'groups': groups,
            'especes': queryset,
            'planting': planting,
            'p_count': p_count
        }

    templateStr = render_to_string("parametres/tab_espece.html", context)
    return JsonResponse({'templateStr': templateStr, 'id': id}, safe=False)


@api_view(['GET'])
def searching_parcelle(request):
    code = request.GET.get('code')
    parcelle = Parcelle.objects.filter(code=code)

    if not parcelle:
        return JsonResponse({'msg': "Desolé, cette parcelle n'existe pas.", "status": 400}, safe=False)
    else:
        templateStr = render_to_string("parametres/carte_recherche.html")
        return JsonResponse({'templateStr': templateStr, 'code': code}, safe=False)


@api_view(['GET'])
def recherche_parcelles(request, code=None, id=None):
    id_parcelle = Parcelle.objects.filter(code=code)
    parcelle1 = Planting.objects.filter(parcelle_id__in=id_parcelle)
    serializer = PlantingSerializer(parcelle1, many=True)
    return Response(serializer.data)


def Plantings(request):
    cooperative = get_object_or_404(Cooperative, id=id)
    querysets = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative).values(
        "parcelle__producteur__cooperative__sigle").annotate(nb_plante=Sum('plant_recus'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['parcelle__producteur__cooperative__sigle'])
        print(labels)
        data.append(stat['plant_recus'])
        print(data)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    # querysets = DetailPlanting.objects.values("planting__parcelle__producteur__cooperative__sigle").aggregate(total=Sum('nb_plante'))['total']
    # # print("querysets")
    # # querysets = DetailPlanting.objects.values("planting__parcelle__producteur__cooperative__sigle").aggregate(total=Sum('nb_plante'))['total']
    # labels = []
    # labels = []
    # data = []
    # for stat in querysets:
    #     labels.append(stat['planting__parcelle__producteur__cooperative__sigle'])
    #     data.append(stat['nb_plante'])
    #
    # return JsonResponse(data= {
    #     'labels':labels,
    #     'data':data,
    # })


def semences_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    semences = Semence_Pepiniere.objects.values("espece_recu__libelle").filter(
        pepiniere__cooperative_id=cooperative).annotate(qte_recu=Sum('qte_recu'))
    labels = []
    data = []
    for stat in semences:
        labels.append(stat['espece_recu__libelle'])
        data.append(stat['qte_recu'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def plantings_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    querysets = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).values(
        "espece__libelle").annotate(nb_plante=Sum('nb_plante'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['espece__libelle'])
        data.append(stat['nb_plante'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def export_prod_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producteurs')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE', 'SECTION', 'LOCALITE', 'CODE', 'TYPE', 'GENRE', 'NOM', 'PRENOMS', 'CONTACTS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'cooperative__sigle',
        'section__libelle',
        'localite',
        'code',
        'type_producteur',
        'genre',
        'nom',
        'prenoms',
        'contacts',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# Export To PDF
def export_prods_to_pdf(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    template_path = 'cooperatives/prods_pdf.html'
    context = {
        'cooperative': cooperative,
        'producteurs': producteurs,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/csv')
    # response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Producteurs.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('Une Erreure est Survenue, Réessayer SVP... <pre>' + html + '</pre>')
    return response


def export_parcelle_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Parcelles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Parcelles')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE', 'SECTION', 'CODE', 'NOM', 'PRENOMS', 'CERTIF', 'CULTURE', 'SUPER', 'LONG', 'LAT']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative.id).values_list(
        'producteur__cooperative__sigle',
        'producteur__section__libelle',
        'code',
        'producteur__nom',
        'producteur__prenoms',
        'certification',
        'culture',
        'superficie',
        'longitude',
        'latitude',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_parcelles_to_pdf(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    template_path = 'cooperatives/parcelles_pdf.html'
    context = {
        'cooperative': cooperative,
        'parcelles': parcelles,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/csv')
    # response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Parcelles.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('Une Erreure est Survenue, Réessayer SVP... <pre>' + html + '</pre>')
    return response


def projet(request):
    projets = Projet.objects.all()
    form = ProjetForm()
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet = projet.save()
        messages.success(request, "Projet Ajoutée avec succès")
        return HttpResponseRedirect(reverse('projets'))
    context = {
        'projets': projets,
        'form': form,
    }
    return render(request, 'projets.html', context)


def update_projet(request, id=None):
    instance = get_object_or_404(Projet, id=id)
    form = ProjetForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.info(request, "Projet Modifié Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('projets'))
    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, "projet_edit.html", context)


def delete_projet(request, id=None):
    item = get_object_or_404(Projet, id=id)
    if request.method == "POST":
        item.delete()
        messages.error(request, "Projet Supprimée Avec Succès")
        return redirect('projets')
    context = {
        # 'pepiniere': pepiniere,
        'item': item,
    }
    return render(request, 'projet_delete.html', context)


def DetailPlantings(request):
    querysets = DetailPlanting.objects.values("espece__libelle").annotate(nb_plante=Sum('nb_plante'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['espece__libelle'])
        data.append(stat['nb_plante'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def plantsparcoop(request, id=None):
    # querysets = Planting.objects.values("parcelle__producteur__cooperative").aggregate(total=Sum('plant_recus'))['total'] #Planting.objects.values("parcelle__producteur__cooperative").annotate(plant_recus=Sum('plant_recus'))
    # labels = []
    # data = []
    # for stat in querysets:
    #     labels.append(stat['parcelle__producteur__cooperative'])
    #     data.append(stat['plant_recus'])
    #
    # return JsonResponse(data={
    #     'labels': labels,
    #     'data': data,
    # })
    cooperative = get_object_or_404(Cooperative, id=id)
    querysets = Planting.objects.values("parcelle__producteur__cooperative__sigle").filter(parcelle__producteur__cooperative_id=cooperative).annotate(plant_recus=Sum('plant_recus'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['parcelle__producteur__cooperative__sigle'])
        # print(labels)
        data.append(stat['plant_recus'])
        # print(data)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def prime(request):
    activate = 'prime'
    primes = Prime.objects.all()
    form = PrimeForm()
    if request.method == 'POST':
        form = PrimeForm(request.POST)
        if form.is_valid():
            prime = form.save(commit=False)
            prime = prime.save()
        messages.success(request, "Prime Ajoutée avec succès")
        return HttpResponseRedirect(reverse('primes'))

    ctx = {
        'primes': primes,
        'form': form,
        'activate':activate
    }
    return render(request, 'parametres/primes.html', ctx)


def production(request):
    activate = 'production'
    productions = Production.objects.all()
    ctx = {
        'productions': productions,
        'activate':activate
    }
    return render(request, 'production.html', ctx)

def cooperative(request):
    activate = 'cooperative'
    cooperatives = Cooperative.objects.all()
    for coop in cooperatives:
        coop.parcelles = Parcelle.objects.filter(producteur__cooperative=coop).count()
        coop.productions = Production.objects.filter(parcelle__producteur__cooperative=coop).aggregate(total=Sum('qteProduct'))['total']
        coop.plants = Planting.objects.filter(parcelle__producteur__cooperative=coop).aggregate(total=Sum('plant_recus'))['total']
        coop.superficies = Parcelle.objects.filter(producteur__cooperative=coop).aggregate(total=Sum('superficie'))['total']
    ctx = {
        'cooperatives' : cooperatives,
        'activate':activate
    }
    return render(request, 'cooperatives.html', ctx)

def producteur(request):
    activate = 'producteur'
    producteurs = Producteur.objects.all()
    for prod in producteurs:
        prod.superficies = Parcelle.objects.filter(producteur=prod).aggregate(total=Sum('superficie'))['total']
    ctx = {
        'producteurs' : producteurs,
        'activate':activate
    }
    return render(request, 'producteurs.html', ctx)

def parcelle(request):
    activate = 'parcelle'
    parcelles = Parcelle.objects.all()
    for p in parcelles:
        p.plants_recus = Planting.objects.filter(parcelle=p).aggregate(total=Sum('plant_recus'))['total']
        p.plants_plante = DetailPlanting.objects.filter(planting__parcelle=p).aggregate(total=Sum('nb_plante'))['total']
    ctx = {
        'parcelles' : parcelles,
        'activate': activate
    }
    return render(request, 'parcelles.html', ctx)


def edit_prime(request,id=None):
    instance = get_object_or_404(Prime, id=id)
    form = PrimeForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
		"instance": instance,
		"form":form,
	}
    
    templateStr = render_to_string("prime/prime_edit.html", context)
    return JsonResponse({'templateStr':templateStr,'id':id},safe=False)



def delete_prime(request,id=None):
    prime = get_object_or_404(Prime, id=id)
    prime.delete()


def update_prime(request):
    id = request.POST['instance_id']
    instance = get_object_or_404(Prime, id=id)
    form = PrimeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return JsonResponse({"msg": "Modification effectuée avec success","status":200,"id": id},safe=False)
    else:
        return JsonResponse({"errors":form.errors,"danger": "Modification incorrect"},safe=False)


@api_view(['GET'])
def map_by_cooperative(request,id=None):
    coop_connect = Cooperative.objects.get(id=id)
    sections  = Section.objects.filter(cooperative_id = coop_connect.id)
    context = {
        "coop_connect":coop_connect,
        "sections": sections
    }

    return render(request, 'cooperatives/usercoop/coop_connect_carte.html',context)


def export_prod_xls(request,id=None):
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
    cooperative = Cooperative.objects.get(id=id)
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


def export_prods_to_pdf(request,id=None):
    cooperative = Cooperative.objects.get(id=id)
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


def export_parcelles_to_pdf(request,id=None):
    cooperative = Cooperative.objects.get(id=id)
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



def export_parcelle_xls(request,id=None):
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
    cooperative = Cooperative.objects.get(id=id)
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


def export_formation_to_pdf(request, id=None):
    formation = get_object_or_404(Formation, id=id)
    cooperative = Cooperative.objects.get(id=formation.cooperative.id)
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

# API'S FOR MOBILES

class CooperativeListView(ListAPIView):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    # print(queryset.count())


class ProducteurListView(ListAPIView):
    queryset = Producteur.objects.all().order_by("nom")
    serializer_class = ProducteurSerializer
    # print(queryset.count())


class ParcelleListView(ListAPIView):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleMobileSerializer


class PlantingListView(ListAPIView):
    queryset = Planting.objects.all()
    serializer_class = PlantingSerializer

class ProductionListView(ListAPIView):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer


class MobilePlantingListView(ListAPIView):
    queryset = DetailPlanting.objects.all()
    serializer_class = DetailsPlantingMobileSerializer