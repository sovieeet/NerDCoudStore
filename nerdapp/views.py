from django.shortcuts import render, redirect
from .models import Categoria, Producto, Subasta
from .forms import CustomUserCreationForm, SubastaForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request,"cuenta creada correctamente")
            return redirect(to="index")
        data["form"] = formulario

    return render(request, 'registration/signup.html', data)

def listSubastas(request):
    subastas = Subasta.objects.all()
    data = {
        "subastas" : subastas
    }
    return render(request, 'subasta/listSubastas.html', data)

def agregarSubasta(request):
    data = {
        'form': SubastaForm()
    }
    if request.method == 'POST':
        formulario = SubastaForm(data=request.POST, files=request.FILES)
        #print("formulario ",formulario)
        if formulario.is_valid:
            formulario.save()
            data['mensaje']="guardado correctamente"
        else:
            data["form"] = formulario
    return render(request, 'subasta/agregarSubasta.html',data)