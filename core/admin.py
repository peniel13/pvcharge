from django.contrib import admin

# Register your models here.


from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from .models import ProjetContribution, Contribution, ProjetRealise, Commune, Contree,City

from django.db.models import Sum
from django.contrib import admin
from .models import ProjetContribution

from django.contrib import admin
from django.db.models import Sum, F, Q
from django.utils.html import format_html
from django.contrib import admin
from django.db.models import Sum, Q, F
from django.utils.html import format_html
from .models import ProjetContribution, Contribution


class ObjectifAtteintFilter(admin.SimpleListFilter):
    title = "Objectif atteint"
    parameter_name = 'objectif_atteint'

    def lookups(self, request, model_admin):
        return (
            ('oui', 'Oui'),
            ('non', 'Non'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(
            total=Sum('contributions__montant', filter=Q(contributions__is_active=True))
        )
        if self.value() == 'oui':
            return queryset.filter(total__gte=F('montant_objectif'))
        elif self.value() == 'non':
            return queryset.filter(total__lt=F('montant_objectif'))
        return queryset


@admin.register(ProjetContribution)
class ProjetContributionAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'montant_objectif',
        'montant_recolte_admin',
        'progression_admin',
        'ville',
        'commune',
        'contree',
        'en_cours',
        'created_at',
        'video_link',
    )
    list_filter = ('ville', 'commune', 'contree', 'en_cours', ObjectifAtteintFilter)
    list_editable = ('en_cours',)
    readonly_fields = ('created_at',)
    search_fields = ('titre', 'description')

    def montant_recolte_admin(self, obj):
        total = obj.contributions.filter(is_active=True).aggregate(Sum('montant'))['montant__sum'] or 0
        return f"{float(total):,.2f} FC"
    montant_recolte_admin.short_description = "Montant récolté"
    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{}" target="_blank">Voir la vidéo</a>', obj.video.url)
        return "—"
    video_link.short_description = "Vidéo"

    readonly_fields = ('created_at',)
    def progression_admin(self, obj):
        total = obj.contributions.filter(is_active=True).aggregate(Sum('montant'))['montant__sum'] or 0
        try:
            if obj.montant_objectif > 0:
                progress = (total / obj.montant_objectif) * 100

                # Auto désactivation (optionnel)
                if total >= obj.montant_objectif and obj.en_cours:
                    obj.en_cours = False
                    obj.save(update_fields=["en_cours"])

                # Affichage conditionnel
                color = "green" if progress >= 100 else "orange" if progress >= 50 else "gray"
                return format_html('<strong style="color:{};">{:.2f}%</strong>', color, progress)
            else:
                return format_html('<span style="color:gray;">N/A</span>')
        except Exception:
            return "Erreur"
    progression_admin.short_description = "Progression"



@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = (
        'nom_contributeur', 'montant', 'projet',
       
        'phone_number', 'id_transaction',
        'date_contribution', 'user', 'is_active'
    )
    list_filter = ( 'is_active', 'date_contribution')
    search_fields = ('nom_contributeur', 'projet__titre', 'id_transaction', 'phone_number')
    readonly_fields = ('date_contribution',)

from django.contrib import admin
from .models import ProjetRealise
from django.utils.html import format_html

@admin.register(ProjetRealise)
class ProjetRealiseAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ville', 'commune', 'contree', 'created_at', 'preview_image', 'video_link')
    list_filter = ('ville', 'commune', 'contree', 'created_at')
    search_fields = ('titre', 'description')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;"/>', obj.image.url)
        return "—"
    preview_image.short_description = "Image"

    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{}" target="_blank">Voir la vidéo</a>', obj.video.url)
        return "—"
    video_link.short_description = "Vidéo"

    readonly_fields = ('created_at',)



admin.site.register(Commune)
admin.site.register(Contree)
admin.site.register(City)
