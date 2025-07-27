from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}))

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic"]



from django import forms
from .models import ProjetContribution, Contribution, ProjetRealise, Commune, Contree

class ProjetContributionForm(forms.ModelForm):
    class Meta:
        model = ProjetContribution
        fields = ['titre', 'description', 'montant_objectif','video', 'image', 'ville', 'commune', 'contree']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['commune'].queryset = Commune.objects.none()
        self.fields['contree'].queryset = Contree.objects.none()

        if 'ville' in self.data:
            try:
                ville_id = int(self.data.get('ville'))
                self.fields['commune'].queryset = Commune.objects.filter(city_id=ville_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'commune' in self.data:
            try:
                commune_id = int(self.data.get('commune'))
                self.fields['contree'].queryset = Contree.objects.filter(commune_id=commune_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['commune'].queryset = Commune.objects.filter(city=self.instance.ville)
            self.fields['contree'].queryset = Contree.objects.filter(commune=self.instance.commune)




from django import forms
from .models import Contribution, Commune, Contree
from django import forms
from .models import Contribution, Commune, Contree
from .models import  Commune, Contree  # et les autres modèles déjà utilisés
class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = [
            'nom_contributeur', 'montant', 'id_transaction', 'phone_number'
        ]
        widgets = {
            'id_transaction': forms.TextInput(attrs={'placeholder': 'ID de transaction'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.pop('projet', None)  # plus nécessaire
        super().__init__(*args, **kwargs)



from django import forms
from .models import ProjetRealise, Commune, Contree, City

class ProjetRealiseForm(forms.ModelForm):
    class Meta:
        model = ProjetRealise
        fields = ['titre', 'description', 'image', 'video', 'ville', 'commune', 'contree']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['commune'].queryset = Commune.objects.none()
        self.fields['contree'].queryset = Contree.objects.none()

        if 'ville' in self.data:
            try:
                ville_id = int(self.data.get('ville'))
                self.fields['commune'].queryset = Commune.objects.filter(city_id=ville_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.ville:
            self.fields['commune'].queryset = Commune.objects.filter(city=self.instance.ville)

        if 'commune' in self.data:
            try:
                commune_id = int(self.data.get('commune'))
                self.fields['contree'].queryset = Contree.objects.filter(commune_id=commune_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.commune:
            self.fields['contree'].queryset = Contree.objects.filter(commune=self.instance.commune)

    def clean(self):
        cleaned_data = super().clean()
        ville = cleaned_data.get('ville')
        commune = cleaned_data.get('commune')
        contree = cleaned_data.get('contree')

        if not ville and not commune and not contree:
            raise forms.ValidationError(
                "Veuillez sélectionner au moins une localisation (ville, commune ou contrée)."
            )
        return cleaned_data
