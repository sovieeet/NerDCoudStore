from django.shortcuts import render, redirect
from .models import Categoria
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return render(request, 'nerdapp/index.html')

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
    return render(request, 'subasta/listSubastas.html')

def agregarSubasta(request):
    return render(request, 'subasta/agregarSubasta.html')