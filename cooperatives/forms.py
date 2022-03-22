from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields, DateInput
from django.http import request
# from django_select2 import forms as s2forms
# from django_select2.forms import ModelSelect2Widget

# class CooperativeWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "sigle__icontains",
#         #"email__icontains",
#     ]
#
# class SectionWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "libelle__icontains",
#         #"email__icontains",
#     ]

from cooperatives.models import Cooperative, Producteur, Section, Sous_Section, Parcelle, Planting, Formation, \
    Detail_Formation, Monitoring, Production
# from cooperatives.views import cooperative
from parametres.models import Region, Projet, Activite, Origine, Sous_Prefecture, Espece

User = get_user_model()
non_allowed_username = ["abc", "123", "admin1", "admin12"]

class UserForm(forms.ModelForm):
    last_name = forms.CharField(label="Nom")
    first_name = forms.CharField(label="Prénoms")
    username = forms.CharField(label="Nom d’utilisateur")
    email = forms.EmailField(label="Adresse électronique")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password", "class": "form-control"}), label="Mot de Passe")

    class Meta:
        model=User
        fields=['last_name','first_name','username', 'email', 'password']

class CoopForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    region=forms.ModelChoiceField(queryset=Region.objects.all(),empty_label="Région")
    projet=forms.ModelChoiceField(queryset=Projet.objects.all(),empty_label="Projet")
    activite=forms.ModelChoiceField(queryset=Activite.objects.all(),empty_label="Natures Activités")
    class Meta:
        model=Cooperative
        fields=[
            'region',
            'sigle',
            'activite',
            'projet',
            'contacts',
            'logo',
        ]

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        widgets = {
            # "cooperative": CooperativeWidget,
            #"co_authors": CoAuthorsWidget,
        }
        fields = [
            'libelle',
            'responsable',
            'contacts',
        ]

class Sous_SectionForm(forms.ModelForm):
    class Meta:
        model = Sous_Section
        fields = [
             'section',
            'libelle',
            'responsable',
            'contacts',
        ]

class Edit_Sous_SectionForm(forms.ModelForm):
    class Meta:
        model = Sous_Section
        fields = [
            'section',
            'libelle',
            'responsable',
            'contacts',
        ]

class ProdForm(forms.ModelForm):
    # origine = forms.ModelChoiceField(queryset=Origine.objects.all(), empty_label="Origine")
    sous_prefecture = forms.ModelChoiceField(queryset=Sous_Prefecture.objects.all())
    # section = forms.ModelChoiceField(queryset=Section.objects.all().fil, empty_label="Section")
    sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section", required=False)
    class Meta:
        model = Producteur
        fields = [
            'code',
            'origine',
            'sous_prefecture',
            'type_producteur',
            'nom',
            'dob',
            'genre',
            'contacts',
            'localite',
            'section',
            'sous_section',
            'nb_enfant',
            'nb_epouse',
            'enfant_scolarise',
            'nb_personne',
            'nb_parcelle',
            'image',
            'type_document',
            'num_document',
            'document',
        ]

class EditProdForm(forms.ModelForm):
    origine = forms.ModelChoiceField(queryset=Origine.objects.all(), empty_label="Origine")
    sous_prefecture = forms.ModelChoiceField(queryset=Sous_Prefecture.objects.all())
    section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label="Section")
    sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section", required=False)
    class Meta:
        model = Producteur
        fields = [
            'code',
            'origine',
            'sous_prefecture',
            'type_producteur',
            'nom',
            'dob',
            'genre',
            'contacts',
            'localite',
            'section',
            'sous_section',
            'nb_enfant',
            'nb_epouse',
            'enfant_scolarise',
            'nb_personne',
            'nb_parcelle',
            'image',
            'type_document',
            'num_document',
            'document',
        ]
        
    def get_cooperative(self, request, *args, **kwargs):
        cooperative = Cooperative.objects.get(user_id=request.user.id)
        producteur_obj = Producteur.objects.filter(cooperative_id=cooperative)
        return producteur_obj

class ParcelleForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    # projet = forms.ModelChoiceField(queryset=Projet.objects.all(), empty_label="Projet")
    # section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label="Section")
    # producteur = forms.ModelChoiceField(queryset=Producteur.objects.all(), empty_label="Propriétaires")
    # sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section",required=False)

    class Meta:
        model=Parcelle
        fields=[
            'code',
            'code_certificat',
            'annee_certificat',
            'annee_acquis',
            #'producteur',
            # 'sous_section',
            'acquisition',
            'latitude',
            'longitude',
            'culture',
            'certification',
            'superficie'
        ]

    #producteur = AutoCompleteField('producteur')
    # def __init__(self, user=None, **kwargs):
    #     super(ParcelleForm, self).__init__(**kwargs)
    #     if user:
    #         cooperative = Cooperative.objects.get(user_id=user)
    #         self.fields['propietaire'].queryset = Parcelle.objects.filter(propietaire__cooperative_id=cooperative)
    #         self.fields['section'].queryset = Parcelle.objects.filter(section__cooperative_id=cooperative)
    #         # self.fields['sous_section']= Parcelle.objects.filter(section__cooperative_id=cooperative)

class EditParcelleForm(forms.ModelForm):

    class Meta:
        model=Parcelle
        fields=[
            'code',
            'producteur',
            # 'sous_section',
            'acquisition',
            'latitude',
            'longitude',
            'culture',
            'certification',
            'superficie'
        ]

class FormationForm(forms.ModelForm):

    class Meta:
        model=Formation
        fields=[
            'formateur',
            'note_formateur',
            'intitule',
            'campagne',            
            'structureformateur',
            'niveauformateur',
            'debut',
            'fin',
            'participant',
            'critere'
        ]

class EditFormationForm(forms.ModelForm):

    class Meta:
        model=Formation
        fields=[
            'formateur',
            'note_formateur',
            'campagne',
            'debut',
            'fin',
        ]

class DetailFormation(forms.ModelForm):
    # participant = forms.ModelMultipleChoiceField(queryset=Producteur.objects.all(), empty_label="Producteurs",required=False)
    # participant = forms.ModelMultipleChoiceField(queryset=Producteur.objects.all())
    participant = forms.CheckboxSelectMultiple()

    class Meta:
        model = Detail_Formation
        fields = [
            # 'formation',
            'participant',
        ]
        # widgets = {
        #     'participant': forms.CheckboxSelectMultiple(),
        # }
        # widgets = {'participant': ModelSelect2Widget(
        #     queryset=Producteur.objects.all().distinct('participant'),
        #     search_fields=['participant_icontains']
        # )}

from django.forms import ModelForm, inlineformset_factory

from .models import DetailMonitoring, MonitoringEspece, Participantcoop, Participantformation, Planting, DetailPlanting, RemplacementMonitoring
# from .models import FamilyMember, Profile


class PlantingForm(ModelForm):
    class Meta:
        model = Planting
        fields = [
            # "parcelle",
            "nb_plant_exitant",
            #"plant_recus",
            "campagne",
            "projet",
            "date",
        ]

class DetailPlantingForm(ModelForm):
    class Meta:
        model = DetailPlanting
        fields = [
            # "planting",
            "espece",
            "nb_plante",
        ]

DetailPlantingFormSet = inlineformset_factory(
    Planting, DetailPlanting, form=DetailPlantingForm, extra=1)


class MonitoringForm(ModelForm):
    class Meta:
        model = Monitoring
        fields = [
            "mort_global",
            "date",
            "mature_global",
            "observation",
            #"planting"
            
        ]

#class DetailMonitoringForm(ModelForm):
#    class Meta:
#        model = DetailMonitoring
#        exclude = ['monitoring',]
        

class MonitoringEspeceForm(ModelForm):
    class Meta:
        model = MonitoringEspece
        fields = [
            "detailmonitoring",
            "espece",
            "detailplanting",
            "mort",
            #"mature",            
        ]


class ParticipantcoopForm(forms.ModelForm):

    class Meta:
        model=Participantcoop
        fields=[
            'nom',
            'contact'
        ]


class ParticipantformationForm(forms.ModelForm):

    class Meta:
        model=Participantformation
        fields=[
            'nom',
          #  'localite',
            'contact'
        ]


class RemplacementMonitoringForm(forms.ModelForm):
    class Meta:
        model=RemplacementMonitoring
        fields=[
            'date',
        ]


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production

        fields = [
            'campagne',
            'qteProduct',
            
            
        ]

class EditProductionForm(forms.ModelForm):
    class Meta:
        model = Production

        fields = [
            #'campagne',
            'parcelle',
            'qteProduct',
        ]