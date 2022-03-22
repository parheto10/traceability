from django.urls import path

from .views import (
    DetailPlantings,
    client_index,
    coopdetailPlantings,
    detail_planting,
    export_formation_to_pdf,
    export_planting_xls,
    plants_par_section,
    projet,
    detail_proj,
    localisation,
    detail_coop,
    # chart,
    prod_coop,
    parcelle_coop,
    localisation_coop,
    section_coop,
    sous_section_coop,
    planting_coop, formations,
    detail_formation,
    export_prod_xls,
    export_parcelle_xls,
    export_prods_to_pdf,
    export_parcelles_to_pdf,
    Plantings, pepiniere, producteur, parcelle, production, planting, prod_coop_par_campagne,
    # export_plant_xls,
    # export_formation_xls,
    # export_prods_to_pdf,
    # export_parcelles_to_pdf,
    # producteursPDF
)

app_name = 'clients'

urlpatterns = [
    # path('', connexion, name='connexion'),
    # path('logout', loggout, name='logout'),
    path('index/', client_index, name='dashboard'),
    path('projets/', projet, name='projets'),
    path('formation/<int:id>', formations, name='formations'),
    path('formation/<int:id>/<int:_id>', detail_formation, name='formation'),
    path('producteurs/<int:id>', prod_coop, name='prod_coop'),
    path('parcelles/<int:id>', parcelle_coop, name='parcelle_coop'),
    path('sections/<int:id>', section_coop, name='section_coop'),
    path('sous_sections/<int:id>', sous_section_coop, name='sous_section_coop'),
    path('planting/<int:id>', planting_coop, name='planting_coop'),
    path('coordonnes/<int:id>', localisation_coop, name='localisation_coop'),
    path('localisation/', localisation, name='localisation'),
    path('Plantings/', Plantings, name='Plantings'),
    path('DetailPlantings/', DetailPlantings, name='DetailPlantings'),
    path('coopdetailPlantings/<int:id>', coopdetailPlantings, name='coopdetailPlantings'),
    path('plants_par_section/<int:id>', plants_par_section, name='plants_par_section'),
    path('prod_coop_par_campagne/<int:id>', prod_coop_par_campagne, name='prod_coop_par_campagne'),

    # path('site_pepinieres/', site_pepinieres, name='site_pepinieres'),
    # path('coop_pepiniere/<int:id>', coop_pepiniere, name='coop_pepiniere'),
    path('detail_proj/<int:id>', detail_proj, name='detail_proj'),
    path('detail_coop/<int:id>', detail_coop, name='detail_coop'),
    # #Charts
    # path('Stats_coop/', Stats_coop, name='stats_coop'),
    # path('Stats_semences/', Stats_semences, name='stats_semences'),
    # path('Production_plan/', Production_plan, name='production_plan'),
    # path('plants_coop/<int:id>', plants_coop, name='plants_coop'),
    # path('semences_coop/<int:id>', semences_coop, name='semences_coop'),
    # path('chart/<int:id>', chart, name='chart'),
    #
    # #Export to Excel
    path('cooperative/<int:id>/producteurs/xls/', export_prod_xls, name='export_prod_xls'),
    # # path('sections/xls/', export_section_xls, name='export_section_xls'),
    # # path('sous_sections/xls/', export_sous_section_xls, name='export_sous_section_xls'),
    path('cooperative/<int:id>/parcelles/xls/', export_parcelle_xls, name='export_parcelle_xls'),
    # path('cooperative/<int:id>/plants/xls/', export_plant_xls, name='export_plant_xls'),
    # path('cooperative/<int:id>/formations/xls/', export_formation_xls, name='export_formation_xls'),
    #
    # # Export Données EN PDF
    path('producteurs/pdf/<int:id>', export_prods_to_pdf, name='export_prods_to_pdf'),
    # path('producteurs/pdf/<int:id>', producteursPDF, name='prods_to_pdf'),
    path('parcelles/pdf/<int:id>', export_parcelles_to_pdf, name='export_parcelles_to_pdf'),

    path('pepinieres/', pepiniere, name='pepinieres'),

    path('export_formation_to_pdf/<int:id>', export_formation_to_pdf, name='export_formation_to_pdf'),

    path('producteurs/', producteur, name='producteurs'),
    path('parcelles/', parcelle, name='parcelles'),
    path('productions/', production, name='productions'),
    path('plantings/', planting, name='plantings'),
    path('plantings/<int:id>', detail_planting, name='suivi_planting'),
    path('export_planting_xls/', export_planting_xls, name='export_planting_xls'),
]
