from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def signup(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            user.save()
            messages.success(request, "Compte créé avec succès !")
            return redirect("signin")
        else:
            # Afficher les erreurs du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {"form": form}
    return render(request, "core/signup.html", context)


def signin (request):
    if request.method == 'POST':
        email = request.POST["email"]
        password= request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context= {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Contribution

@login_required
def profile(request):
    user = request.user

    # 🔹 Contributions actives faites par l'utilisateur
    contributions_actives = Contribution.objects.filter(user=user, is_active=True).select_related('projet')

    context = {
        "user": user,
        "contributions_actives": contributions_actives,
        # 🔁 Tu peux aussi ajouter ici d'autres données comme les stores du user
    }

    return render(request, "core/profile.html", context)



@login_required
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
                
    context = {"form": form}
    return render(request, "core/update_profile.html", context)



from django.shortcuts import render, get_object_or_404
from .models import City, Commune, Contree, ProjetRealise

# ✔️ Vue liste des villes
from django.db.models import Sum

from django.db.models import Count

def city_list_view(request):
    cities = City.objects.all()

    for city in cities:
        # Nombre de communes liées à cette ville
        city.nb_communes = city.communes.count()

        # Projets de contribution ciblant directement la ville
        projets_directs = ProjetContribution.objects.filter(ville=city)

        # Projets globaux (aucune ville/commune/contrée définie)
        projets_globaux = ProjetContribution.objects.filter(
            ville__isnull=True, commune__isnull=True, contree__isnull=True
        )

        projets_valides = projets_directs | projets_globaux

        city.nb_projets_contribution = projets_valides.distinct().count()

        # Projets réalisés dans cette ville
        city.nb_projets_realises = ProjetRealise.objects.filter(ville=city).count()

    return render(request, 'core/city_list.html', {'cities': cities})



# ✔️ Vue détail d'une ville

from django.db.models import Q
from django.db.models import Q
def city_detail_view(request, city_id):
    city = get_object_or_404(City, id=city_id)
    communes = Commune.objects.filter(city=city)
    projets_realises = ProjetRealise.objects.filter(ville=city)
     # ➕ Enrichir chaque commune avec ses statistiques
    for commune in communes:
        commune.nb_contrees = commune.contrees.count()
        commune.nb_projets_realises = ProjetRealise.objects.filter(commune=commune).count()
        commune.nb_projets_contribution = ProjetContribution.objects.filter(commune=commune).count()
        
    projets_cibles = ProjetContribution.objects.filter(ville=city)
    projets_globaux = ProjetContribution.objects.filter(
        ville__isnull=True, commune__isnull=True, contree__isnull=True
    )
    projets_contribution = projets_cibles | projets_globaux

    projets = []
    for projet in projets_contribution.distinct():
        montant_recolte = projet.contributions.filter(is_active=True).aggregate(
            Sum('montant')
        )['montant__sum'] or 0
        projet.montant_recolte_effectif = montant_recolte
        projet.objectif_atteint = montant_recolte >= projet.montant_objectif
        projets.append(projet)

    return render(request, 'core/city_detail.html', {
        'city': city,
        'communes': communes,
        'nb_communes': communes.count(),
        'nb_projets_realises': projets_realises.count(),
        'nb_projets_contribution': len(projets),
        'projets': projets_realises,
        'projets_contribution': projets,
    })



# ✔️ Vue détail d'une commune
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from core.models import Commune, Contree, ProjetRealise, ProjetContribution

def commune_detail_view(request, commune_id):
    commune = get_object_or_404(Commune, id=commune_id)
    contrees = Contree.objects.filter(commune=commune)

    # ➕ Enrichir chaque contree avec ses statistiques
    for contree in contrees:
        contree.nb_projets_realises = ProjetRealise.objects.filter(contree=contree).count()
        contree.nb_projets_contribution = ProjetContribution.objects.filter(contree=contree).count()

    projets_realises = ProjetRealise.objects.filter(commune=commune)

    projets_cibles = ProjetContribution.objects.filter(commune=commune)
    projets_globaux = ProjetContribution.objects.filter(
        ville__isnull=True, commune__isnull=True, contree__isnull=True
    )
    projets_contribution = projets_cibles | projets_globaux

    projets = []
    for projet in projets_contribution.distinct():
        montant_recolte = projet.contributions.filter(is_active=True).aggregate(
            Sum('montant')
        )['montant__sum'] or 0
        projet.montant_recolte_effectif = montant_recolte
        projet.objectif_atteint = montant_recolte >= projet.montant_objectif
        projets.append(projet)

    return render(request, 'core/commune_detail.html', {
        'commune': commune,
        'contrees': contrees,
        'nb_contrees': contrees.count(),
        'nb_projets_realises': projets_realises.count(),
        'nb_projets_contribution': len(projets),
        'projets': projets_realises,
        'projets_contribution': projets,
    })




from django.db.models import Sum
def contree_detail_view(request, contree_id):
    contree = get_object_or_404(Contree, id=contree_id)
    projets_realises = ProjetRealise.objects.filter(contree=contree)

    projets_cibles = ProjetContribution.objects.filter(contree=contree)
    projets_globaux = ProjetContribution.objects.filter(
        ville__isnull=True, commune__isnull=True, contree__isnull=True
    )
    projets_contribution = projets_cibles | projets_globaux

    projets = []
    for projet in projets_contribution.distinct():
        montant_recolte = projet.contributions.filter(is_active=True).aggregate(
            Sum('montant')
        )['montant__sum'] or 0
        projet.montant_recolte_effectif = montant_recolte
        projet.objectif_atteint = montant_recolte >= projet.montant_objectif
        projets.append(projet)

    return render(request, 'core/contree_detail.html', {
        'contree': contree,
        'nb_projets_realises': projets_realises.count(),
        'nb_projets_contribution': len(projets),
        'projets': projets_realises,
        'projets_contribution': projets,
    })



from django.shortcuts import render, get_object_or_404
from .models import ProjetContribution, City, Commune, Contree

# ✅ Tous les projets de contribution
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from .models import ProjetContribution

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum

def projet_contribution_list(request):
    projets_contribution = ProjetContribution.objects.all().order_by('-created_at')

    projets = []
    for projet in projets_contribution:
        montant_recolte = projet.contributions.filter(is_active=True).aggregate(
            Sum('montant')
        )['montant__sum'] or 0
        projet.montant_recolte_effectif = montant_recolte
        projet.objectif_atteint = montant_recolte >= projet.montant_objectif
        projets.append(projet)

    # ✅ Pagination
    paginator = Paginator(projets, 6)  # 6 projets par page
    page = request.GET.get('page')

    try:
        projets_page = paginator.page(page)
    except PageNotAnInteger:
        projets_page = paginator.page(1)
    except EmptyPage:
        projets_page = paginator.page(paginator.num_pages)

    return render(request, 'core/projet_contribution_list.html', {
        'projets': projets_page,
        'title': "Tous les projets"
    })



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def projets_contribution_globaux_view(request):
    projets_list = ProjetContribution.objects.filter(
        ville__isnull=True,
        commune__isnull=True,
        contree__isnull=True
    ).order_by('-created_at')

    paginator = Paginator(projets_list, 6)  # 🔢 6 projets par page
    page = request.GET.get('page')

    try:
        projets = paginator.page(page)
    except PageNotAnInteger:
        projets = paginator.page(1)
    except EmptyPage:
        projets = paginator.page(paginator.num_pages)

    return render(request, 'core/projet_contribution_list.html', {
        'projets': projets,
        'title': "Projets de contribution globaux"
    })


# ✅ Projets d’une ville
def projet_contribution_by_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    projets = ProjetContribution.objects.filter(ville=city).order_by('-created_at')
    return render(request, 'core/projet_contribution_list.html', {
        'projets': projets,
        'title': f"Projets pour la ville de {city.name}"
    })

# ✅ Projets d’une commune
def projet_contribution_by_commune(request, commune_id):
    commune = get_object_or_404(Commune, id=commune_id)
    projets = ProjetContribution.objects.filter(commune=commune).order_by('-created_at')
    return render(request, 'core/projet_contribution_list.html', {
        'projets': projets,
        'title': f"Projets pour la commune de {commune.name}"
    })

# ✅ Projets d’une contrée
def projet_contribution_by_contree(request, contree_id):
    contree = get_object_or_404(Contree, id=contree_id)
    projets = ProjetContribution.objects.filter(contree=contree).order_by('-created_at')
    return render(request, 'core/projet_contribution_list.html', {
        'projets': projets,
        'title': f"Projets pour la contrée de {contree.name}"
    })


from .models import Contribution

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from .models import ProjetContribution, Contribution

from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import ProjetContribution, Contribution

def contributions_for_projet_view(request, projet_id):
    projet = get_object_or_404(ProjetContribution, id=projet_id)

    query = request.GET.get('q', '').strip()
    contributions_list = Contribution.objects.filter(projet=projet, is_active=True)

    # 🔍 Filtrer par nom du contributeur si une recherche est faite
    if query:
        contributions_list = contributions_list.filter(nom_contributeur__icontains=query)

    contributions_list = contributions_list.order_by('-date_contribution')

    paginator = Paginator(contributions_list, 10)  # 🔁 10 contributions par page
    page_number = request.GET.get('page')

    try:
        contributions = paginator.page(page_number)
    except PageNotAnInteger:
        contributions = paginator.page(1)
    except EmptyPage:
        contributions = paginator.page(paginator.num_pages)

    montant_recolte = contributions_list.aggregate(Sum('montant'))['montant__sum'] or 0
    projet.montant_recolte_effectif = montant_recolte

    return render(request, 'core/contributions_list.html', {
        'projet': projet,
        'contributions': contributions,
        'search_query': query,  # Pour garder la valeur dans le champ de recherche
    })





from django.shortcuts import render, get_object_or_404, redirect
from .models import ProjetContribution
from .forms import ContributionForm
from django.contrib import messages

# def contribution_create_view(request, projet_id):
#     projet = get_object_or_404(ProjetContribution, pk=projet_id)

#     if not projet.en_cours:
#         messages.warning(request, "Ce projet n'est plus ouvert aux contributions.")
#         return redirect('projet_contribution_detail', projet_id=projet.id)

#     if request.method == 'POST':
#         form = ContributionForm(request.POST)
#         if form.is_valid():
#             contribution = form.save(commit=False)
#             contribution.projet = projet
#             if request.user.is_authenticated:
#                 contribution.user = request.user
#             contribution.save()
#             messages.success(request, "Merci pour votre contribution ! Elle sera validée après vérification.")
#             return redirect('projet_contribution_detail', projet_id=projet.id)
#     else:
#         form = ContributionForm()

#     return render(request, 'core/contribution_form.html', {
#         'form': form,
#         'projet': projet
#     })
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import ProjetContribution, Contribution
from .forms import ContributionForm

def contribution_create_view(request, projet_id):
    projet = get_object_or_404(ProjetContribution, pk=projet_id)

    if not projet.en_cours:
        messages.warning(request, "Ce projet n'est plus ouvert aux contributions.")
        return redirect('projet_contribution_detail', projet_id=projet.id)

    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.projet = projet
            if request.user.is_authenticated:
                contribution.user = request.user
            contribution.save()

            messages.success(request, "Merci pour votre contribution ! Elle sera validée après vérification.")
            return redirect('projet_contribution_detail', projet_id=projet.id)
    else:
        form = ContributionForm()

    return render(request, 'core/contribution_form.html', {
        'form': form,
        'projet': projet
    })





from django.http import JsonResponse
from .models import Commune, Contree

def api_communes(request):
    ville_id = request.GET.get('ville')
    communes = Commune.objects.filter(city_id=ville_id).values('id', 'name')
    return JsonResponse(list(communes), safe=False)

def api_contrees(request):
    commune_id = request.GET.get('commune')
    contrees = Contree.objects.filter(commune_id=commune_id).values('id', 'name')
    return JsonResponse(list(contrees), safe=False)

from django.http import JsonResponse
from .models import Commune, Contree

def get_communes_by_ville(request):
    ville_id = request.GET.get('ville')
    communes = Commune.objects.filter(city_id=ville_id).values('id', 'name')
    return JsonResponse(list(communes), safe=False)

def get_contrees_by_commune(request):
    commune_id = request.GET.get('commune')
    contrees = Contree.objects.filter(commune_id=commune_id).values('id', 'name')
    return JsonResponse(list(contrees), safe=False)

from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Commune, Contree

def load_communes(request):
    ville_id = request.GET.get('ville_id')
    communes = Commune.objects.filter(city_id=ville_id)
    html = render_to_string('core/commune_dropdown_list_options.html', {'communes': communes})
    return JsonResponse(html, safe=False)

def load_contrees(request):
    commune_id = request.GET.get('commune_id')
    contrees = Contree.objects.filter(commune_id=commune_id)
    html = render_to_string('core/contree_dropdown_list_options.html', {'contrees': contrees})
    return JsonResponse(html, safe=False)


from django.db.models import Sum

def projet_contribution_detail_view(request, projet_id):
    projet = get_object_or_404(ProjetContribution, id=projet_id)

    montant_recolte = projet.contributions.filter(is_active=True).aggregate(Sum('montant'))['montant__sum'] or 0
    objectif_atteint = montant_recolte >= projet.montant_objectif

    return render(request, 'core/projet_contribution_detail.html', {
        'projet': projet,
        'montant_recolte_effectif': montant_recolte,
        'objectif_atteint': objectif_atteint,
    })


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from core.models import ProjetRealise

def projets_realises_list_view(request):
    projets_list = ProjetRealise.objects.all().order_by('-created_at')

    paginator = Paginator(projets_list, 6)  # 6 projets par page
    page = request.GET.get('page')

    try:
        projets = paginator.page(page)
    except PageNotAnInteger:
        projets = paginator.page(1)
    except EmptyPage:
        projets = paginator.page(paginator.num_pages)

    return render(request, 'core/projets_realises_list.html', {
        'projets': projets,
        'title': "Projets réalisés"
    })


from django.shortcuts import render, get_object_or_404
from core.models import ProjetRealise

def projet_realise_detail_view(request, projet_id):
    projet = get_object_or_404(ProjetRealise, id=projet_id)
    return render(request, 'core/projet_realise_detail.html', {
        'projet': projet,
    })

