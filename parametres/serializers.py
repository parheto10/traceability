# from django.contrib.auth.models import User
# from rest_framework import serializers
#
# from cooperatives.models import Producteur, Parcelle, Section, Sous_Section, Cooperative, Formation, Planting, DetailPlanting
# from parametres.models import Pepiniere, Projet, Projet_Cat, Campagne, Espece, Cat_Plant, Origine, Sous_Prefecture
# from clients.models import Client
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'username',
#             'last_name',
#             'first_name'
#         )
#
# class OrigineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Origine
#         fields = (
#             'id',
#             'code',
#             'pays'
#         )
#
# class SousPrefectureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sous_Prefecture
#         fields = (
#             'id',
#             'libelle',
#         )
#
# class CampagneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Campagne
#         fields = (
#             'id',
#             'titre',
#             'mois_debut',
#             'annee_debut',
#             'mois_fin',
#             'annee_fin'
#         )
#
# class CategorieEspeceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cat_Plant
#         fields = (
#             'id',
#             'libelle',
#     )
#
# class EspeceSerializer(serializers.ModelSerializer):
#     categorie = CategorieEspeceSerializer(read_only=True)
#     class Meta:
#         model = Espece
#         fields = (
#             'id',
#             'categorie',
#             'accronyme',
#             'libelle',
#         )
#     #     depth = 1
#     # def to_representation(self, instance):
#     #     response = super().to_representation(instance)
#     #     response['categorie'] = CategorieEspeceSerializer(instance.categorie).data
#     #     return response
#
# class ClientSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Client
#         fields = (
#             'id',
#             'user',
#             'sigle',
#             'contacts',
#             'libelle',
#             'pays',
#             'adresse',
#             'telephone1',
#             'telephone2',
#             'email',
#             'siteweb',
#             'logo',
#         )
#
# class CategorieProjetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Projet_Cat
#         fields = (
#             'id',
#             "libelle"
#         )
#
# class ProjetSerializer(serializers.ModelSerializer):
#     # categorie = CategorieProjetSerializer(read_only=True)
#     class Meta:
#         model = Projet
#         fields = (
#             'id',
#             "categorie",
#             "titre",
#             "chef",
#             "debut",
#             "fin",
#             "etat",
#         )
#         depth = 1
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['categorie'] = CategorieProjetSerializer(instance.categorie).data
#         return response
#
# class CooperativeSerializer(serializers.ModelSerializer):
#     # projet = ProjetSerializer(many=True)
#     class Meta:
#         model=Cooperative
#         fields = (
#             'id',
#             'user',
#             'region',
#             'sigle',
#             'projet',
#             'contacts',
#             'logo',
#         )
#         depth = 1
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         # response['region'] = ClientSerializer(instance.client).data
#         # response['projet'] = ProjetSerializer(instance.projet).data
#         return response
#
# class SectionSerializer(serializers.ModelSerializer):
#     # cooperative = CooperativeSerializer(read_only=True)
#     class Meta:
#         model = Section
#         fields = (
#             'id',
#             "cooperative",
#             'libelle',
#             'responsable',
#             'contacts',
#         )
#         depth = 1
#     # def to_representation(self, instance):
#     #     response = super().to_representation(instance)
#     #     response['cooperative'] = CooperativeSerializer(instance.cooperative).data
#     #     # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
#     #     return response
#
# class SousSectionSerializer(serializers.ModelSerializer):
#     section = SectionSerializer(read_only=True)
#     class Meta:
#         model = Sous_Section
#         fields = (
#             'id',
#             'libelle',
#             'responsable',
#             'contacts',
#             'section',
#         )
#     #     depth = 1
#     # def to_representation(self, instance):
#     #     response = super().to_representation(instance)
#     #     response['section'] = SectionSerializer(instance.section).data
#     #     # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
#     #     return response
#
# class ProducteurSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Producteur
#         fields = (
#             'id',
#             'code',
#             'origine',
#             'sous_prefecture',
#             'type_producteur',
#             'nom',
#             'dob',
#             'genre',
#             'contacts',
#             'localite',
#             'section',
#             'sous_section',
#             'nb_parcelle',
#             'image',
#             'type_document',
#             'num_document',
#             'document',
#         )
#         depth = 1
#
#
# class ParcelleSerializer(serializers.ModelSerializer):
#     #producteur = ProducteurSerializer(many=True)
#     class Meta:
#         model=Parcelle
#         fields = (
#             'id',
#             'code',
#             'producteur',
#             'acquisition',
#             'latitude',
#             'longitude',
#             'culture',
#             'certification',
#             'superficie'
#         )
#         depth = 1
#
#     #def to_representation(self, instance):
#     #    response = super().to_representation(instance)
#     #    response['producteur'] = ProducteurSerializer(instance.producteur).data
#      #   return response
#
# class FormationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Formation
#         fields = [
#             'cooperative',
#             'projet',
#             'formateur',
#             'libelle',
#             'details',
#             'observation',
#             'debut',
#             'fin',
#         ]
#         depth = 1
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['cooperative'] = CooperativeSerializer(instance.cooperative).data
#         response['projet'] = ProjetSerializer(instance.projet).data
#         return response
#
# class PlantingSerializer(serializers.ModelSerializer):
#     campagne = CampagneSerializer(read_only=True)
#     parcelle = ParcelleSerializer(read_only=True)
#     class Meta:
#         model = Planting
#         fields = (
#             'id',
#             "campagne",
#             "parcelle",
#             "nb_plant_exitant",
#             "plant_recus",
#             "plant_total",
#             "projet",
#             "date",
#         )
#         depth = 1
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['parcelle'] = ParcelleSerializer(instance.parcelle).data
#         # response['projet'] = ProjetSerializer(instance.projet).data
#         # response['campagne'] = CampagneSerializer(instance.campagne).data
#         return response
#
# class DetailsPlantingSerializer(serializers.ModelSerializer):
#     planting = PlantingSerializer(read_only=True)
#     espece = EspeceSerializer(read_only=True)
#     class Meta:
#         model = DetailPlanting
#         fields = (
#             'id',
#             "planting",
#             "espece",
#             "nb_plante",
#         )
#         depth = 1
#
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         # response['planting'] = PlantingSerializer(instance.planting).data
#         # response['espece'] = EspeceSerializer(instance.espece).data
#         # response['campagne'] = CampagneSerializer(instance.campagne).data
#         return response
#
#
#
# class PepiniereSerializer(serializers.ModelSerializer):
#     #producteur = ProducteurSerializer(many=True)
#     class Meta:
#         model=Pepiniere
#         fields=(
#             'id',
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
#         )
#         depth = 1
#
#     #def to_representation(self, instance):
#     #    response = super().to_representation(instance)
#     #    response['producteur'] = ProducteurSerializer(instance.producteur).data
#      #   return response
#
#
#
#


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from cooperatives.models import Producteur, Parcelle, Section, Sous_Section, Cooperative, Formation, Planting, DetailPlanting, Production
from parametres.models import Pepiniere, Projet, Projet_Cat, Campagne, Espece, Cat_Plant, Origine, Sous_Prefecture
from clients.models import Client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'first_name'
        )

class OrigineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origine
        fields = (
            'id',
            'code',
            'pays'
        )

class SousPrefectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sous_Prefecture
        fields = (
            'id',
            'libelle',
        )

class CampagneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campagne
        fields = (
            'id',
            'titre',
            'mois_debut',
            'annee_debut',
            'mois_fin',
            'annee_fin'
        )

class CategorieEspeceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat_Plant
        fields = (
            'id',
            'libelle',
    )

class EspeceSerializer(serializers.ModelSerializer):
    categorie = CategorieEspeceSerializer(read_only=True)
    class Meta:
        model = Espece
        fields = (
            'id',
            'categorie',
            'accronyme',
            'libelle',
        )
    #     depth = 1
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['categorie'] = CategorieEspeceSerializer(instance.categorie).data
    #     return response

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Client
        fields = (
            'id',
            'user',
            'sigle',
            'contacts',
            'libelle',
            'pays',
            'adresse',
            'telephone1',
            'telephone2',
            'email',
            'siteweb',
            'logo',
        )

class CategorieProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet_Cat
        fields = (
            'id',
            "libelle"
        )

class ProjetSerializer(serializers.ModelSerializer):
    # categorie = CategorieProjetSerializer(read_only=True)
    class Meta:
        model = Projet
        fields = (
            'id',
            "categorie",
            "titre",
            "chef",
            "debut",
            "fin",
            "etat",
        )
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['categorie'] = CategorieProjetSerializer(instance.categorie).data
        return response

class CooperativeSerializer(serializers.ModelSerializer):
    # projet = ProjetSerializer(many=True)
    # producteurs = serializers.StringRelatedField(many=True)

    total_producteurs = serializers.SerializerMethodField(read_only=True)
    # total_parcelles = serializers.SerializerMethodField(read_only=True)

    def get_total_producteurs(self, Cooperative):
        return Cooperative.producteurs.count()

    class Meta:
        model=Cooperative
        fields = (
            'id',
            'user',
            'region',
            'sigle',
            'projet',
            'contacts',
            'logo',
            # 'producteurs',
            'total_producteurs',
        )
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['region'] = ClientSerializer(instance.client).data
        # response['projet'] = ProjetSerializer(instance.projet).data
        return response

class SectionSerializer(serializers.ModelSerializer):
    # cooperative = CooperativeSerializer(read_only=True)
    class Meta:
        model = Section
        fields = (
            'id',
            "cooperative",
            'libelle',
            'responsable',
            'contacts',
        )
        depth = 1
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['cooperative'] = CooperativeSerializer(instance.cooperative).data
    #     # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
    #     return response

class SousSectionSerializer(serializers.ModelSerializer):
    section = SectionSerializer(read_only=True)
    class Meta:
        model = Sous_Section
        fields = (
            'id',
            'libelle',
            'responsable',
            'contacts',
            'section',
        )
    #     depth = 1
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['section'] = SectionSerializer(instance.section).data
    #     # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
    #     return response

class ProducteurSerializer(serializers.ModelSerializer):
    cooperative = serializers.StringRelatedField()
    origine = serializers.StringRelatedField()
    sous_prefecture = serializers.StringRelatedField()
    section = serializers.StringRelatedField()
    class Meta:
        model = Producteur
        fields = (
            'id',
            'code',
            'origine',
            'sous_prefecture',
            'genre',
            'type_producteur',
            'nom',
            'dob',
            'genre',
            'contacts',
            'localite',
            'nb_enfant',
            'nb_epouse',
            'section',
            'sous_section',
            'nb_parcelle',
            'image',
            'type_document',
            'num_document',
            'document',
            'cooperative',
            'origine',
        )
        depth = 1


class ParcelleSerializer(serializers.ModelSerializer):
    #producteur = ProducteurSerializer(many=True)
    class Meta:
        model=Parcelle
        fields = (
            'id',
            'code',
            'producteur',
            'acquisition',
            'latitude',
            'longitude',
            'culture',
            'certification',
            'superficie'
        )
        depth = 1

    #def to_representation(self, instance):
    #    response = super().to_representation(instance)
    #    response['producteur'] = ProducteurSerializer(instance.producteur).data
     #   return response

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = [
            'cooperative',
            'projet',
            'formateur',
            'libelle',
            'details',
            'observation',
            'debut',
            'fin',
        ]
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cooperative'] = CooperativeSerializer(instance.cooperative).data
        response['projet'] = ProjetSerializer(instance.projet).data
        return response

class PlantingMobileSerializer(serializers.ModelSerializer):
    # campagne = CampagneSerializer(read_only=True)
    # parcelle = ParcelleSerializer(read_only=True)
    campagne = serializers.StringRelatedField()
    parcelle = serializers.StringRelatedField()
    projet = serializers.StringRelatedField()

    # total_monitoring = serializers.SerializerMethodField(read_only=True)
    #
    # # total_parcelles = serializers.SerializerMethodField(read_only=True)
    #
    # def get_total_monitoring(self, Planting):
    #     return Parcelle.monitorings.count()

    class Meta:
        model = Planting
        fields = (
            'id',
            "campagne",
            "parcelle",
            "nb_plant_exitant",
            "plant_recus",
            "plant_total",
            "projet",
            "date",
        )
        depth = 1
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['parcelle'] = ParcelleSerializer(instance.parcelle).data
    #     # response['projet'] = ProjetSerializer(instance.projet).data
    #     # response['campagne'] = CampagneSerializer(instance.campagne).data
    #     return response


class PlantingSerializer(serializers.ModelSerializer):
    campagne = CampagneSerializer(read_only=True)
    parcelle = ParcelleSerializer(read_only=True)
    class Meta:
        model = Planting
        fields = (
            'id',
            "campagne",
            "parcelle",
            "nb_plant_exitant",
            "plant_recus",
            "plant_total",
            "projet",
            "date",
        )
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['parcelle'] = ParcelleSerializer(instance.parcelle).data
        # response['projet'] = ProjetSerializer(instance.projet).data
        # response['campagne'] = CampagneSerializer(instance.campagne).data
        return response

class DetailsPlantingSerializer(serializers.ModelSerializer):
    planting = PlantingSerializer(read_only=True)
    espece = EspeceSerializer(read_only=True)
    class Meta:
        model = DetailPlanting
        fields = (
            'id',
            "planting",
            "espece",
            "nb_plante",
        )
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['planting'] = PlantingSerializer(instance.planting).data
        # response['espece'] = EspeceSerializer(instance.espece).data
        # response['campagne'] = CampagneSerializer(instance.campagne).data
        return response


class DetailsPlantingMobileSerializer(serializers.ModelSerializer):
    planting = PlantingSerializer(read_only=True)
    espece = EspeceSerializer(read_only=True)
    class Meta:
        model = DetailPlanting
        fields = (
            'id',
            "planting",
            "espece",
            "nb_plante",
        )
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['planting'] = PlantingSerializer(instance.planting).data
        response['espece'] = EspeceSerializer(instance.espece).data
        # response['campagne'] = CampagneSerializer(instance.campagne).data
        return response



class PepiniereSerializer(serializers.ModelSerializer):
    #producteur = ProducteurSerializer(many=True)
    class Meta:
        model=Pepiniere
        fields=(
            'id',
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
            #'fournisseur',
            #'contacts_fournisseur',
            'sachet_recus',
            'production_plant',
            'production_realise',
            'plant_mature',
            'plant_retire',
        )
        depth = 1

    #def to_representation(self, instance):
    #    response = super().to_representation(instance)
    #    response['producteur'] = ProducteurSerializer(instance.producteur).data
     #   return response


class ParcelleMobileSerializer(serializers.ModelSerializer):
    # total_monitoring = serializers.SerializerMethodField(read_only=True)
    # plantings = serializers.StringRelatedField(many=True)
    # total_plantings = serializers.SerializerMethodField(read_only=True)
    #
    # def get_total_plantings(self, Parcelle):
    #     return Parcelle.plantings.count()

    producteur = serializers.StringRelatedField()
    class Meta:
        model=Parcelle
        fields = (
            'id',
            'code',
            'producteur',
            'acquisition',
            'latitude',
            'longitude',
            'culture',
            'certification',
            'superficie',
            # 'code_certificat',
            # 'annee_certificat',
            # 'annee_acquis',
            # 'plantings',
            # 'total_plantings',
            # 'get_total_plantings',
        )
        depth = 1

    def to_representation(self, instance):
       response = super().to_representation(instance)
       response['producteur'] = ProducteurSerializer(instance.producteur).data
       return response

class ProductionSerializer(serializers.ModelSerializer):
    parcelle = serializers.StringRelatedField()
    campagne = serializers.StringRelatedField()
    class Meta:
        model = Production
        fields = (
            'id',
            'parcelle',
            'campagne',
            'annee',
            'qteProduct',
        )

