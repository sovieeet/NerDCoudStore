from bootstrap_datepicker_plus.widgets  import DatePickerInput, TimePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from .models import Subasta, ParticiparSubasta, Usuario


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
        model = ParticiparSubasta
        fields = '__all__'

"""
class ListarYParticiparSubastas(View):
    def get(self, request, *args, **kwargs):
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
        subastas = Subasta.objects.all()
        data = {
            "subastas" : subastas,
        }
        return render(request, 'subasta/listSubastas.html', data)
    def post(self, request, *args, **kwargs):
        class Meta:
            model = ParticiparSubasta
            fields = '__all__'
        print("La función participarSubasta se está ejecutando.")
        data = {
            'form': ParticiparSubastaForm()
        }
        if request.method == 'POST':
            formulario = ParticiparSubastaForm(data=request.POST, files=request.FILES)
            if formulario.is_valid:
                usuario = Usuario.objects.get(id_usuario=request.usuario_id)             
                subasta = Subasta.objects.get(subasta_id = request.subasta_id)
                montoS = request.POST.get('monto')
                print("Usuario:", usuario)
                print("Subasta:", subasta)
                print("Monto:", montoS)
               participarSubastaUsuario = ParticiparSubasta.objects.create(
                    usuario_id_usuario_id=usuario,
                    subasta_id_subasta_id=subasta,
                    monto=montoS
                )
                participarSubastaUsuario.save()
                data['mensaje']="guardado correctamente"
            else:
                data["form"] = formulario"""