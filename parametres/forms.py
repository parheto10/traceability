# from django import forms
# from django.contrib.auth import get_user_model
# #from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.forms import ModelForm
#
# from parametres.models import Fournisseur, Pepiniere, Projet, Semence_Pepiniere
#
# User = get_user_model()
# non_allowed_username = ["abc", "123", "admin1", "admin12"]
#
# class LoginForm(forms.Form):
#     username = forms.CharField(label="Nom Utilisateur")
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password"}), label="Mot de Passe")
#
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         qs = User.objects.filter(username__iexact=username)
#         if not qs.exists:
#             raise forms.ValidationError("Utilisateur Invalide !!!")
#         return username
#
# class UserForm(forms.ModelForm):
#     last_name = forms.CharField(label="Nom")
#     first_name = forms.CharField(label="Prénoms")
#     username = forms.CharField(label="Nom d’utilisateur")
#     email = forms.EmailField(label="Adresse électronique")
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password", "class": "form-control"}), label="Mot de Passe")
#
#     class Meta:
#         model=User
#         fields=['last_name', 'first_name', 'username', 'email', 'password']
#
# # class ProjetForm(ModelForm):
# #     class Meta:
# #         model = Projet
# #         fields = [
# #             'client',
# #             'categorie',
# #             'accronyme',
# #             'titre',
# #             'chef',
# #             'debut',
# #             'fin',
# #             'etat',
# #         ]
#
#
#
# # #for contact us page
# # class ContactForm(forms.Form):
# #     Nom = forms.CharField(max_length=30)
# #     Email = forms.EmailField()
# #     Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
#
#
# class PepiniereForm(forms.ModelForm):
#
#     class Meta:
#         model=Pepiniere
#         fields=[
#             'projet',
#             'campagne',
#             'region',
#             'ville',
#             'site',
#             'latitude',
#             'longitude',
#             'technicien',
#             'contacts_technicien',
#             'superviseur',
#             'contacts_superviseur',
#             #'fournisseur',
#             #'contacts_fournisseur',
#             'sachet_recus',
#             'production_plant',
#             'production_realise',
#             'plant_mature',
#             'plant_retire',
#         ]
#
# class FournisseurForm(forms.ModelForm):
#
#     class Meta:
#         model=Fournisseur
#         fields=[
#             'pseudo',
#             'ville',
#             'localite',
#             'contact',
#
#         ]
#
#
#
#
#
# class SemenceForm(forms.ModelForm):
#
#     class Meta:
#         model=Semence_Pepiniere
#         fields=[
#             'fournisseur',
#             'espece_recu',
#             'production',
#             'qte_recu',
#             'date',
#             'details',
#         ]
#
#
#

from django import forms
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from parametres.models import Fournisseur, Pepiniere, Projet, Semence_Pepiniere, Prime

User = get_user_model()
non_allowed_username = ["abc", "123", "admin1", "admin12"]


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom Utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}), label="Mot de Passe")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists:
            raise forms.ValidationError("Utilisateur Invalide !!!")
        return username


class UserForm(forms.ModelForm):
    last_name = forms.CharField(label="Nom")
    first_name = forms.CharField(label="Prénoms")
    username = forms.CharField(label="Nom d’utilisateur")
    email = forms.EmailField(label="Adresse électronique")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password", "class": "form-control"}),
                               label="Mot de Passe")

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email', 'password']


class ProjetForm(ModelForm):
    class Meta:
        model = Projet
        fields = [
            # 'client',
            'categorie',
            'sigle',
            'titre',
            'chef',
            'debut',
            'fin',
            'etat',
        ]


# #for contact us page
# class ContactForm(forms.Form):
#     Nom = forms.CharField(max_length=30)
#     Email = forms.EmailField()
#     Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class PepiniereForm(forms.ModelForm):
    class Meta:
        model = Pepiniere
        fields = [
            'projet',
            'campagne',
            'region',
            'ville',
            'site',
            'latitude',
            'longitude',
            'technicien',
            'contacts_technicien',
            'superviseur',
            'contacts_superviseur',
            # 'fournisseur',
            # 'contacts_fournisseur',
            'sachet_recus',
            'production_plant',
            'production_realise',
            'plant_mature',
            'plant_retire',
        ]


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = [
            'pseudo',
            'ville',
            'localite',
            'contact',

        ]


class SemenceForm(forms.ModelForm):
    class Meta:
        model = Semence_Pepiniere
        fields = [
            'fournisseur',
            'espece_recu',
            'production',
            'qte_recu',
            'date',
            'details',
        ]

class PrimeForm(forms.ModelForm):
    class Meta:
        model = Prime
        fields = [
            'campagne',
            'libelle',
            'prix',
        ]

