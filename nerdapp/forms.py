from bootstrap_datepicker_plus.widgets  import DatePickerInput, TimePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subasta
<<<<<<< HEAD

=======
from .models import Usuario_subasta
>>>>>>> origin/manuel

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

<<<<<<< HEAD
class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'
class SubastaForm(forms.models.ModelForm):
    class Meta:
        db_table = 'nerdapp_subasta'
        model = Subasta
        #fields = ['imagen','nombre','descripcion','precio_inicial','fecha_termino','hora_termino' ]
        fields = '__all__'
        widgets = {
            'fecha_termino' : DatePickerInput(),
            'hora_termino' : TimePickerInput(),
            'id_subasta': forms.HiddenInput(),
        }
=======
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
>>>>>>> origin/manuel
