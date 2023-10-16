from django.shortcuts import render
from .models import Categoria
from django.contrib.auth.views import LoginView

def hola_mundo(request):
    return render(request, 'nerdapp/index.html')

def dashboard(request):
    return render(request, 'nerdapp/dashboard.html')

def page2(request):
    return render(request, 'nerdapp/page2.html')

def lista_categorias(request):
    categorias = Categoria.objects.all()
    print(categorias)
    return render(request, 'nerdapp/lista_categorias.html', {'categorias': categorias})

class CustomLoginView(LoginView):
    template_name = 'nerdapp/login.html'