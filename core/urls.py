from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),  # Redirige vers allauth
    path('signout',views.signout, name='signout'),
    path('profile/',views.profile, name='profile'),
    path('update_profile/',views.update_profile, name='update_profile'),
    # 🌆 Liste des villes
    path('villes/', views.city_list_view, name='city_list'),

    # 🏙️ Détail d'une ville
    path('villes/<int:city_id>/', views.city_detail_view, name='city_detail'),

    # 🏘️ Détail d'une commune
    path('communes/<int:commune_id>/', views.commune_detail_view, name='commune_detail'),

    # 🏡 Détail d'une contrée
    path('contrees/<int:contree_id>/', views.contree_detail_view, name='contree_detail'),
    
    path('projets/', views.projet_contribution_list, name='projet_contribution_list'),
    path('projets/ville/<int:city_id>/', views.projet_contribution_by_city, name='projet_contribution_by_city'),
    path('projets/commune/<int:commune_id>/', views.projet_contribution_by_commune, name='projet_contribution_by_commune'),
    path('projets/contree/<int:contree_id>/', views.projet_contribution_by_contree, name='projet_contribution_by_contree'),
    path('projets/<int:projet_id>/contributions/', views.contributions_for_projet_view, name='contributions_for_projet'),
    path('contribution/<int:projet_id>/create/', views.contribution_create_view, name='contribution_create'),
    path('api/communes/', views.api_communes, name='api_communes'),
    path('api/contrees/', views.api_contrees, name='api_contrees'),
    path('api/communes/', views.get_communes_by_ville, name='api_communes_by_ville'),
    path('api/contrees/', views.get_contrees_by_commune, name='api_contrees_by_commune'),
    path('ajax/load-communes/', views.load_communes, name='load_communes'),
    path('ajax/load-contrees/', views.load_contrees, name='load_contrees'),
    path('user/projets/<int:projet_id>/', views.projet_contribution_detail_view, name='projet_contribution_detail'),
    path('projets-realises/', views.projets_realises_list_view, name='projets_realises_list'),
    path('projets-realises/<int:projet_id>/', views.projet_realise_detail_view, name='projet_realise_detail'),
    
]


