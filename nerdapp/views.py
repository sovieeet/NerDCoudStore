import datetime
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Categoria, Producto, Subasta, Usuario_subasta, Usuario, ParticiparSubasta
from .forms import CustomUserCreationForm, SubastaForm, ParticiparSubastaForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail

def index(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }

    return render(request, 'nerdapp/index.html', data)

def dashboard(request):
    return render(request, 'nerdapp/dashboard.html')

def page2(request):
    return render(request, 'nerdapp/page2.html')

def lista_categorias(request):
    categorias = Categoria.objects.all()
    print(categorias)
    return render(request, 'nerdapp/lista_categorias.html', {'categorias': categorias})

def listForo(request):
    return render(request, 'foro/listForo.html')

def signup(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            aux_user = formulario.save()
            usuario = Usuario.objects.create(
                id_usuario = aux_user.id,
                nombre_usuario = aux_user.username,
                nombre = aux_user.first_name,
                apellido = aux_user.last_name,
                correo = aux_user.email,        
            )
            usuario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request,"cuenta creada correctamente")
            return redirect(to="index")
        data["form"] = formulario

    return render(request, 'registration/signup.html', data)
def agregarSubasta(request):
    data = {
        'form': SubastaForm()
    }
    if request.method == 'POST':
        formulario = SubastaForm(data=request.POST, files=request.FILES)
        #print("formulario ",formulario)
        if formulario.is_valid:
            subasta = formulario.save()  # Guarda la subasta y obtén la instancia
            usuario = Usuario.objects.get(id_usuario=request.user.id)  # Obtiene el usuario actual
            usuario_subasta = Usuario_subasta.objects.create(
                usuario_id_usuario=usuario,  # Obtiene el id del usuario actual
                subasta_id_subasta=subasta # Usa el id de la subasta recién creada
            )
            usuario_subasta.save()  # Guarda la relación en UsuarioSubasta
            data['mensaje']="guardado correctamente"
        else:
            data["form"] = formulario
    return render(request, 'subasta/agregarSubasta.html',data)

class ListarYParticiparSubastas(View):
    def get(self, request, *args, **kwargs):
        subastas = Subasta.objects.all().order_by('-fecha_inicio')
        form = ParticiparSubastaForm()
        context = {
            'subastas': subastas,
            'form': form,
        }
        return render(request, 'subasta/listSubastas.html', context)
    def post(self, request, *args, **kwargs):
        formulario = ParticiparSubastaForm(data=request.POST, files=request.FILES)
        subastas = Subasta.objects.all().order_by('-fecha_inicio')
        context = {
            'subastas': subastas,
            'form': formulario,
        }
        usuario =request.POST.get('usuario_id')           
        subasta = request.POST.get('subasta_id')
        montoS = request.POST.get('monto')
        subastaClass = Subasta.objects.get(id_subasta=subasta)
        print("Usuario:", usuario)
        print("Subasta:", subasta)
        print("precio_inicial:", subastaClass.precio_inicial)
        print("precio_mas_alto:", subastaClass.precio_mas_alto)
        print("Monto:", montoS)
        if formulario.is_valid and int(montoS) > int(subastaClass.precio_inicial) and int(montoS) >  int(subastaClass.precio_mas_alto) :
            usuarioClass = Usuario.objects.get(id_usuario=request.user.id)      
            participarSubastaUsuario = ParticiparSubasta.objects.create(
                usuario_id_usuario_id=usuarioClass,
                subasta_id_subasta_id=subastaClass,
                monto=montoS
            )
            participarSubastaUsuario.save()
            subastaClass.precio_mas_alto = montoS
            subastaClass.save()
            return redirect(reverse('participacionSubasta', args=[subasta, montoS]))
        elif  int(montoS) < int(subastaClass.precio_inicial) :
            context['mensaje'] = 'El monto ingresado es menor a la oferta mas alta'
        else:
            context['mensaje'] = 'Hubo un error al procesar el formulario. Por favor, inténtelo de nuevo.'

        return render(request, 'subasta/listSubastas.html', context)

def participacionSubasta(request, subasta_id, monto):
    print("Subasta:", subasta_id)
    print("Monto:", monto)
    try:
        subasta = Subasta.objects.get(id_subasta=subasta_id)
        context = {
            'subasta': subasta,
            'descripcion' : subasta.descripcion,
            'fecha_termino' : subasta.fecha_termino,
            'hora_termino' : subasta.hora_termino,
            'monto': monto,
        }
        return render(request, 'subasta/participacionSubasta.html', context)
    except Subasta.DoesNotExist:
        return HttpResponse("Subasta no encontrada.")

"""
def enviar_correo(subasta):
    subject = 'Subasta finalizada'
    message = f'La subasta {subasta.nombre} ha finalizado. ¡Felicidades! Tu oferta de ${subasta.precio_mas_alto} ha ganado.'
    from_email = 'your-email@example.com'
    recipient_list = [subasta.usuario_id_usuario_id.correo]  # Dirección de correo del usuario que ganó la subasta

    send_mail(subject, message, from_email, recipient_list)
"""