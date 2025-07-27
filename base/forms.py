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
from .models import Store, StoreManager, Product, StockEntry, Sale
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'location', 'image', 'devise']



class StoreManagerForm(forms.ModelForm):
    class Meta:
        model = StoreManager
        fields = ['user', 'store']


from django import forms
from core.models import Product  # adapte si nécessaire selon ton arborescence

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['store', 'manager']  # ✅ Ces champs sont définis dans la vue
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),
        }


from django import forms
from .models import StockEntry

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['product', 'quantity_added', 'purchase_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),
            'quantity_added': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2',
                'step': '0.01',
                'placeholder': 'Prix d\'achat en FC'
            }),
        }



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold']


# forms.py
from django import forms
from core.models import DailyRegisterPhoto

class DailyRegisterPhotoForm(forms.ModelForm):
    class Meta:
        model = DailyRegisterPhoto
        fields = ['image']
