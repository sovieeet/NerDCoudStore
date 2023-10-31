from bootstrap_datepicker_plus.widgets  import DatePickerInput, TimePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subasta, ParticiparSubasta


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

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
    def __init__(self, *args, **kwargs):
        super(SubastaForm, self).__init__(*args, **kwargs)
        self.fields['precio_mas_alto'].initial = 0
        self.fields['precio_mas_alto'].widget = forms.HiddenInput()

class ParticiparSubastaForm(forms.models.ModelForm):
    class Meta:
        db_table = 'nerdapp_participarsubasta'
        model = ParticiparSubasta
        fields = '__all__'
        