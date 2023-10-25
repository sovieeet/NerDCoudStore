from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subasta
from .models import Usuario_subasta

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

class SubastaForm(forms.ModelForm):
    class Meta:
        db_table = 'nerdapp_subasta'
        model = Subasta
        fields = '__all__'
        widgets = {
            'id_subasta': forms.HiddenInput(),
        }

class UsuarioSubastaForm(forms.ModelForm):
    class Meta:
        db_table = 'nerdapp_usuario_subasta'
        model = Usuario_subasta
        fields = '__all__'