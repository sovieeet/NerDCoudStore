from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Categoria, Producto, Subasta, Usuario_subasta, Usuario, ParticiparSubasta
from .forms import CustomUserCreationForm, SubastaForm, ParticiparSubastaForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q

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
"""def listSubastas(request):
    subastas = Subasta.objects.all()
    data = {
        "subastas" : subastas,
    }
    return render(request, 'subasta/listSubastas.html', data)


def participarSubasta(request):
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
            data["form"] = formulario
    #return render(request, 'subasta/agregarSubasta.html')
"""

class ListarYParticiparSubastas(View):
    def get(self, request, *args, **kwargs):
        subastas = Subasta.objects.all()
        form = ParticiparSubastaForm()
        context = {
            'subastas': subastas,
            'form': form,
        }
        return render(request, 'subasta/listSubastas.html', context)
    def post(self, request, *args, **kwargs):
        formulario = ParticiparSubastaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid:
            usuario =request.POST.get('usuario_id')           
            subasta = request.POST.get('subasta_id')
            montoS = request.POST.get('monto')
            print("Usuario:", usuario)
            print("Subasta:", subasta)
            print("Monto:", montoS)
            """participarSubastaUsuario = ParticiparSubasta.objects.create(
                usuario_id_usuario_id=usuario,
                subasta_id_subasta_id=subasta,
                monto=montoS
            )
            participarSubastaUsuario.save()"""
            return render(request, 'subasta/listSubastas.html')
        subastas = Subasta.objects.all()
        context = {
            'subastas': subastas,
            'form': formulario,
        }
        return render(request, 'listSubastas.html', context)



"""def participarSubasta(request):
    if request.method == 'POST':
        subasta_id = request.POST.get('subasta_id')
        usuario_id = request.POST.get('usuario_id')
        monto = request.POST.get('monto')
        participacion = ParticiparSubasta.objects.create(
            usuario_id_usuario_id= usuario_id,
            subasta_id_subasta_id = subasta_id,
            monto=monto,
        )
        participacion.save()
        messages.success(request,"participacion creada correctamente")
        return HttpResponse('Participación guardada exitosamente')
        
    else:
        return HttpResponse('Método no permitido')"""
