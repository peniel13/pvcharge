from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify # type: ignore
from decimal import Decimal

# Create your models here.


class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
     
    def __str__(self):
        return self.email
    


class City(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cities/", blank=True, null=True)

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='communes')

    def __str__(self):
        return f"{self.name} ({self.city.name})"

class Contree(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='contrees')

    def __str__(self):
        return f"{self.name} ({self.commune.name})"


class ProjetRealise(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projets_realises/')
    video = models.FileField(upload_to='videos_projets/', null=True, blank=True)  # ✅ Facultatif
    ville = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    contree = models.ForeignKey(Contree, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class ProjetContribution(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    montant_objectif = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='projets_contribution/')
    en_cours = models.BooleanField(default=True)
    video = models.FileField(upload_to='videos_projets_contribution/', null=True, blank=True)  # ✅ Facultatif
    ville = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    contree = models.ForeignKey(Contree, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def montant_recolte_effectif(self):
        total = self.contributions.filter(is_active=True).aggregate(models.Sum('montant'))['montant__sum']
        return total or 0

    def progression_pourcent(self):
        if self.montant_objectif > 0:
            return round((self.montant_recolte_effectif() / self.montant_objectif) * 100, 2)
        return 0


from django.conf import settings
class Contribution(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contributions'
    )
    nom_contributeur = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    projet = models.ForeignKey(ProjetContribution, on_delete=models.CASCADE, related_name='contributions')
    id_transaction = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    date_contribution = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom_contributeur} - {self.montant} FC"


