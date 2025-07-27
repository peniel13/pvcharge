from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.db.models import Sum, Count
from core.models import ProjetRealise, Contribution, Commune

from django.db.models import Count, Sum
from django.shortcuts import render
from core.models import ProjetRealise, Contribution, Commune, City, Contree

from django.db.models import Sum, Count, Q
from core.models import ProjetRealise, Contribution, Commune, City, Contree, ProjetContribution

def index(request):
    total_projets_realises = ProjetRealise.objects.count()
    total_contributeurs = Contribution.objects.filter(is_active=True).values('phone_number').distinct().count()
    total_montant_collecte = Contribution.objects.filter(is_active=True).aggregate(Sum('montant'))['montant__sum'] or 0

    total_communes_actives = Commune.objects.annotate(
        nb_projets=Count('projetrealise')
    ).filter(nb_projets__gt=0).count()
    total_communes = Commune.objects.count()

    total_villes_actives = City.objects.annotate(
        nb_projets=Count('projetrealise')
    ).filter(nb_projets__gt=0).count()
    total_villes = City.objects.count()

    total_contrees_actives = Contree.objects.annotate(
        nb_projets=Count('projetrealise')
    ).filter(nb_projets__gt=0).count()
    total_contrees = Contree.objects.count()

    # Liste des villes avec infos supplémentaires
    cities = City.objects.all()
    for city in cities:
        city.nb_communes = city.communes.count()

        projets_directs = ProjetContribution.objects.filter(ville=city)
        projets_globaux = ProjetContribution.objects.filter(
            ville__isnull=True, commune__isnull=True, contree__isnull=True
        )
        projets_valides = projets_directs | projets_globaux
        city.nb_projets_contribution = projets_valides.distinct().count()

        city.nb_projets_realises = ProjetRealise.objects.filter(ville=city).count()
    
    # ✅ Projets de contribution
    projets_contribution = ProjetContribution.objects.all().order_by('-created_at')[:10]  # max 10 pour scroll
    for projet in projets_contribution:
        montant_recolte = projet.contributions.filter(is_active=True).aggregate(
            Sum('montant')
        )['montant__sum'] or 0
        projet.montant_recolte_effectif = montant_recolte
        projet.objectif_atteint = montant_recolte >= projet.montant_objectif    
    
    # ✅ Projets réalisés (max 10 pour scroll horizontal)
    projets_realises = ProjetRealise.objects.all().order_by('-created_at')[:10]    

    return render(request, 'base/index.html', {
        'total_projets_realises': total_projets_realises,
        'total_contributeurs': total_contributeurs,
        'total_montant_collecte': total_montant_collecte,
        'total_communes_actives': total_communes_actives,
        'total_communes': total_communes,
        'total_villes_actives': total_villes_actives,
        'total_villes': total_villes,
        'total_contrees_actives': total_contrees_actives,
        'total_contrees': total_contrees,
        'cities': cities,
        'projets': projets_contribution,
        'projets_realises': projets_realises
    })




def apropos(request):
    return render(request,'base/apropos.html')